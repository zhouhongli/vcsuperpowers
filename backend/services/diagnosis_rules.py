# backend/services/diagnosis_rules.py
"""诊断规则库"""
from typing import Dict, List, Tuple


# 规则结构：异常类型 -> (关键词，根因描述，解决方案列表)
DIAGNOSIS_RULES: Dict[str, Dict] = {
    "NullPointerException": {
        "name": "空指针异常",
        "keywords": {
            "null": "对象引用为空",
            "getinstance()": "获取实例失败",
            "getobject()": "获取对象失败",
            "request": "请求对象为空",
            "response": "响应对象未初始化",
            "context": "上下文对象缺失",
        },
        "root_cause_template": "代码尝试访问空对象的方法或属性。{matched_info}",
        "solutions": [
            "检查对象初始化逻辑，确保在使用前已正确初始化",
            "在访问对象前添加 null 检查或使用 Optional 包装",
            "review 调用链，确保上游返回有效值而非 null",
            "使用 IDE 的 nullability 注解（@Nullable, @NotNull）辅助检测",
        ]
    },
    "TimeoutError": {
        "name": "超时错误",
        "keywords": {
            "connection": "网络连接超时",
            "read": "读取数据超时",
            "database": "数据库查询超时",
            "api": "外部 API 调用超时",
            "socket": "Socket 连接超时",
            "gateway": "网关超时",
        },
        "root_cause_template": "操作超过预设时间限制未完成。{matched_info}",
        "solutions": [
            "检查网络连通性和目标服务状态",
            "增加超时阈值（如 connectTimeout, readTimeout）",
            "添加重试机制（指数退避策略）",
            "分析慢查询并优化数据库索引",
            "考虑添加缓存层减少直接调用",
        ]
    },
    "DatabaseError": {
        "name": "数据库错误",
        "keywords": {
            "constraint": "违反数据库约束",
            "deadlock": "检测到死锁",
            "connection": "连接池耗尽",
            "foreign key": "外键约束冲突",
            "duplicate": "唯一键冲突",
            "transaction": "事务回滚",
        },
        "root_cause_template": "数据库操作失败。{matched_info}",
        "solutions": [
            "检查数据完整性和约束条件",
            "分析事务隔离级别和锁策略",
            "调整连接池配置（maxSize, timeout）",
            "review SQL 语句和索引设计",
            "考虑分库分表或读写分离",
        ]
    },
    "AuthenticationError": {
        "name": "认证错误",
        "keywords": {
            "token": "Token 过期或无效",
            "expired": "凭证已过期",
            "permission": "权限不足",
            "unauthorized": "未授权访问",
            "session": "会话失效",
            "credential": "凭据错误",
        },
        "root_cause_template": "认证或授权失败。{matched_info}",
        "solutions": [
            "刷新认证 Token 或重新登录",
            "检查 Token 有效期配置",
            "验证用户权限配置是否正确",
            "检查认证服务（如 OAuth provider）状态",
            "清除客户端缓存的旧凭证",
        ]
    },
    "Other": {
        "name": "其他异常",
        "keywords": {},
        "root_cause_template": "未分类的异常类型，需要进一步分析日志内容。",
        "solutions": [
            "查看完整的堆栈跟踪定位问题代码",
            "搜索类似问题的历史日志",
            "联系相关服务负责人协助分析",
            "考虑升级到大模型进行深度诊断",
        ]
    }
}


def match_rule(exception_type: str, content: str, stack_trace: str = None) -> Tuple[float, Dict, List[str]]:
    """
    匹配诊断规则

    Returns:
        (score, rule_info, matched_keywords)
        score: 匹配置信度 0-1
        rule_info: 匹配的规则详情
        matched_keywords: 匹配到的关键词列表
    """
    rule = DIAGNOSIS_RULES.get(exception_type, DIAGNOSIS_RULES["Other"])

    if not rule["keywords"]:
        return (0.5, rule, [])

    # 合并搜索文本
    search_text = f"{content} {stack_trace or ''}".lower()

    matched = []
    for keyword, meaning in rule["keywords"].items():
        if keyword.lower() in search_text:
            matched.append(f"{keyword}: {meaning}")

    # 计算置信度
    if matched:
        score = min(0.8 + len(matched) * 0.05, 1.0)
    else:
        score = 0.5

    return (score, rule, matched)
