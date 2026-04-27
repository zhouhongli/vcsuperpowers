# backend/services/diagnosis_llm.py
"""大模型诊断引擎（Claude API 降级）"""
import json
import os
import re
from typing import Optional, Dict, Any


DIAGNOSIS_PROMPT = """你是一位资深系统诊断专家。请分析以下日志并生成诊断报告：

【日志内容】
{content}

【异常类型】
{exception_type}

【严重程度】
{severity}

【服务名称】
{service_name}

【堆栈跟踪】
{stack_trace}

请按以下格式输出诊断结果（JSON）：
{{
    "root_cause": "根因分析，200 字以内",
    "solution": "建议解决方案，分步骤列出",
    "severity_assessment": "LOW/MEDIUM/HIGH/CRITICAL",
    "confidence": 0.0到1.0的数值
}}
"""

LLM_FALLBACK_RULE = {
    "name": "大模型诊断",
    "root_cause_template": "日志内容较为复杂，已由大模型辅助分析。请查看以下诊断结果。",
    "solutions": [
        "查看大模型生成的根因分析",
        "根据建议方案逐一排查",
        "如问题仍未解决，请手动分析日志内容",
    ],
}


def call_llm(
    exception_type: str,
    content: str,
    severity: str,
    service_name: Optional[str],
    stack_trace: Optional[str],
) -> Optional[Dict[str, Any]]:
    """
    调用大模型进行诊断

    Returns:
        解析后的诊断结果，或 None（调用失败时）
    """
    api_key = os.environ.get("CLAUDE_API_KEY", "")
    if not api_key:
        return None

    try:
        raw_response = _call_claude_api(
            DIAGNOSIS_PROMPT.format(
                content=content,
                exception_type=exception_type,
                severity=severity,
                service_name=service_name or "未指定",
                stack_trace=stack_trace or "无",
            )
        )
        return parse_llm_response(raw_response)
    except Exception:
        return None


def _call_claude_api(prompt: str) -> str:
    """
    调用 Claude API

    使用 Anthropic Messages API
    """
    import httpx

    api_key = os.environ.get("CLAUDE_API_KEY", "")
    model = os.environ.get("CLAUDE_MODEL", "claude-3-5-haiku-20241022")

    response = httpx.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": model,
            "max_tokens": 1024,
            "messages": [
                {"role": "user", "content": prompt},
            ],
        },
        timeout=60.0,
    )
    response.raise_for_status()
    data = response.json()
    return data["content"][0]["text"]


def parse_llm_response(raw: str) -> Optional[Dict[str, Any]]:
    """
    解析 LLM 响应，提取 JSON

    支持纯 JSON 和 Markdown 代码块格式
    """
    # 尝试提取 Markdown 代码块中的 JSON
    markdown_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', raw)
    if markdown_match:
        raw = markdown_match.group(1).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None
