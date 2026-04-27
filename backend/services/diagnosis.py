# backend/services/diagnosis.py
"""诊断服务"""
from typing import Dict, Any, Optional, List
from datetime import datetime

from .diagnosis_rules import match_rule
from .diagnosis_llm import call_llm


class DiagnosisService:
    """诊断服务"""

    def __init__(self, repository):
        self.repository = repository
        self._diagnoses: Dict[str, Dict[str, Any]] = {}

    def diagnose(self, log_id: str) -> Dict[str, Any]:
        """
        诊断指定日志

        流程：
        1. 规则匹配（高置信度直接返回）
        2. 规则匹配失败时降级到大模型
        3. 大模型也失败时返回通用诊断
        """
        log = self.repository.get(log_id)
        if not log:
            raise ValueError(f"Log '{log_id}' not found")

        # 检查是否已有诊断
        if log_id in self._diagnoses:
            return self._diagnoses[log_id]

        # 规则匹配
        score, rule, matched_keywords = match_rule(
            log["exception_type"],
            log["content"],
            log.get("stack_trace")
        )

        # 规则高置信度或分数 >= 0.7 直接返回
        use_llm = score < 0.7 or log["exception_type"] == "Other"
        root_cause = None
        solution = None

        if use_llm:
            # 尝试大模型
            llm_result = call_llm(
                log["exception_type"],
                log["content"],
                log["severity"],
                log.get("service_name"),
                log.get("stack_trace"),
            )
            if llm_result:
                root_cause = llm_result.get("root_cause", rule.get("root_cause_template", ""))
                llm_solution = llm_result.get("solution")
                if llm_solution:
                    solution = llm_solution
                llm_confidence = llm_result.get("confidence")
                if isinstance(llm_confidence, (int, float)):
                    score = float(llm_confidence)

        # 大模型也失败，使用规则匹配结果
        if not root_cause:
            matched_info = (
                f"匹配到关键词：{', '.join(matched_keywords)}"
                if matched_keywords else "未匹配到特定关键词"
            )
            root_cause = rule["root_cause_template"].format(matched_info=matched_info)
            solution = "\n".join(f"{i+1}. {s}" for i, s in enumerate(rule["solutions"]))

        # 查找相似日志
        similar_logs = self._find_similar_logs(log, exclude_id=log_id, limit=3)

        # 构建诊断结果
        diagnosis_data = {
            "id": f"diag-{log_id}",
            "log_id": log_id,
            "root_cause": root_cause,
            "solution": solution,
            "severity_assessment": self._assess_severity(log["severity"], score),
            "similar_logs": similar_logs,
            "created_at": datetime.now().isoformat(),
        }

        self._diagnoses[log_id] = diagnosis_data
        return diagnosis_data

    def get_diagnosis(self, log_id: str) -> Optional[Dict[str, Any]]:
        """获取诊断结果"""
        return self._diagnoses.get(log_id)

    def has_diagnosis(self, log_id: str) -> bool:
        """检查是否已有诊断"""
        return log_id in self._diagnoses

    def _find_similar_logs(self, log: Dict[str, Any], exclude_id: str, limit: int = 3) -> List[str]:
        """
        查找相似日志

        基于异常类型 + 严重程度匹配
        """
        all_logs = self.repository.get_all(page=1, page_size=100)["items"]

        similar = []
        for item in all_logs:
            if item["id"] == exclude_id:
                continue
            if (item["exception_type"] == log["exception_type"] and
                item["severity"] == log["severity"]):
                similar.append(item["id"])
                if len(similar) >= limit:
                    break

        return similar

    def _assess_severity(self, log_severity: str, confidence: float) -> str:
        """
        评估严重程度

        结合日志本身严重程度和诊断置信度
        """
        if log_severity == "CRITICAL":
            return "CRITICAL"
        elif log_severity == "HIGH" or (log_severity == "MEDIUM" and confidence < 0.6):
            return "HIGH"
        return log_severity
