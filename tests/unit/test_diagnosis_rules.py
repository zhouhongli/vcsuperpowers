# tests/unit/test_diagnosis_rules.py
"""诊断规则测试"""
import pytest
from backend.services.diagnosis_rules import match_rule, DIAGNOSIS_RULES


def test_match_nullpointer_with_keywords():
    """测试 NullPointerException 匹配"""
    content = "Cannot invoke method on null object"
    stack_trace = "at Service.getInstance(Service.java:42)"

    score, rule, matched = match_rule("NullPointerException", content, stack_trace)

    assert score >= 0.8
    assert rule["name"] == "空指针异常"
    assert any("null" in m for m in matched) or any("getinstance()" in m for m in matched)


def test_match_timeout_with_database():
    """测试 TimeoutError 数据库场景"""
    content = "Database query timeout after 30s"

    score, rule, matched = match_rule("TimeoutError", content)

    assert score >= 0.8
    assert any("database" in m for m in matched)


def test_match_no_keywords():
    """测试无关键词匹配"""
    content = "Something went wrong"

    score, rule, matched = match_rule("NullPointerException", content)

    assert score == 0.5
    assert len(matched) == 0


def test_match_other_type():
    """测试 Other 类型"""
    content = "Unknown error occurred"

    score, rule, matched = match_rule("Other", content)

    assert score == 0.5
    assert rule["name"] == "其他异常"


def test_case_insensitive_match():
    """测试大小写不敏感匹配"""
    content = "NULL pointer EXCEPTION"

    score, rule, matched = match_rule("NullPointerException", content)

    assert any("null" in m for m in matched)
