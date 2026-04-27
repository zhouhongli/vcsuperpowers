# tests/unit/test_diagnosis_llm.py
"""大模型降级单元测试"""
import json
import os
from unittest.mock import patch, MagicMock

from backend.services.diagnosis_llm import call_llm, parse_llm_response


def test_parse_llm_response_valid_json():
    """解析合法的 LLM JSON 响应"""
    raw = json.dumps({
        "root_cause": "内存溢出",
        "solution": "1. 增加堆内存\n2. 检查内存泄漏",
        "severity_assessment": "HIGH",
        "confidence": 0.85,
    })
    result = parse_llm_response(raw)
    assert result["root_cause"] == "内存溢出"
    assert result["severity_assessment"] == "HIGH"
    assert result["confidence"] == 0.85


def test_parse_llm_response_markdown_block():
    """解析包含 Markdown 代码块的 LLM 响应"""
    raw = """```json
{
    "root_cause": "空指针",
    "solution": "1. 检查",
    "severity_assessment": "MEDIUM",
    "confidence": 0.7
}
```"""
    result = parse_llm_response(raw)
    assert result["root_cause"] == "空指针"
    assert result["confidence"] == 0.7


def test_parse_llm_response_invalid_json():
    """解析非法 JSON 时返回 None"""
    raw = "this is not json at all"
    result = parse_llm_response(raw)
    assert result is None


@patch.dict(os.environ, {"CLAUDE_API_KEY": "test-key"})
@patch('backend.services.diagnosis_llm._call_claude_api')
def test_call_llm_success(mock_claude):
    """成功调用 LLM 并返回解析结果"""
    mock_claude.return_value = json.dumps({
        "root_cause": "测试根因",
        "solution": "1. 测试方案",
        "severity_assessment": "MEDIUM",
        "confidence": 0.9,
    })
    result = call_llm("Other", "test content", "MEDIUM", "test-service", None)
    assert result is not None
    assert result["root_cause"] == "测试根因"
    mock_claude.assert_called_once()


@patch.dict(os.environ, {"CLAUDE_API_KEY": "test-key"})
@patch('backend.services.diagnosis_llm._call_claude_api')
def test_call_llm_when_api_unavailable(mock_claude):
    """LLM API 不可用时返回 None"""
    mock_claude.side_effect = Exception("API unavailable")
    result = call_llm("Other", "test content", "MEDIUM", "test-service", None)
    assert result is None


@patch.dict(os.environ, {}, clear=True)
def test_call_llm_no_api_key():
    """没有设置 API Key 时返回 None"""
    from backend.services.diagnosis_llm import call_llm
    result = call_llm("Other", "test content", "MEDIUM", None, None)
    assert result is None
