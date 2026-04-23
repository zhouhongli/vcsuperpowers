# tests/unit/test_diagnosis_service.py
"""诊断服务测试"""
import pytest
from backend.repository.mock import MockRepository
from backend.services.diagnosis import DiagnosisService


@pytest.fixture
def repo():
    """测试夹具"""
    r = MockRepository()
    yield r
    r.clear()


@pytest.fixture
def service(repo):
    """诊断服务夹具"""
    return DiagnosisService(repo)


@pytest.fixture
def sample_log(repo):
    """创建测试日志"""
    return repo.create({
        "content": "Null pointer when calling getInstance()",
        "exception_type": "NullPointerException",
        "severity": "HIGH",
        "stack_trace": "at com.example.Service.getInstance(Service.java:42)"
    })


def test_diagnose_log(service, repo, sample_log):
    """测试诊断日志"""
    result = service.diagnose(sample_log["id"])

    assert result["log_id"] == sample_log["id"]
    assert "root_cause" in result
    assert "solution" in result
    assert "severity_assessment" in result
    assert "similar_logs" in result


def test_diagnose_not_found(service):
    """测试诊断不存在的日志"""
    with pytest.raises(ValueError, match="not found"):
        service.diagnose("non-existent-id")


def test_diagnosis_cached(service, repo, sample_log):
    """测试诊断结果缓存"""
    # 第一次诊断
    result1 = service.diagnose(sample_log["id"])
    # 第二次获取（应返回缓存）
    result2 = service.get_diagnosis(sample_log["id"])

    assert result1 == result2


def test_has_diagnosis(service, repo, sample_log):
    """测试检查诊断存在"""
    assert not service.has_diagnosis(sample_log["id"])
    service.diagnose(sample_log["id"])
    assert service.has_diagnosis(sample_log["id"])


def test_find_similar_logs(service, repo, sample_log):
    """测试查找相似日志"""
    # 创建相似日志
    repo.create({
        "content": "Another NPE",
        "exception_type": "NullPointerException",
        "severity": "HIGH",
    })
    repo.create({
        "content": "Yet another NPE",
        "exception_type": "NullPointerException",
        "severity": "HIGH",
    })

    result = service.diagnose(sample_log["id"])

    assert len(result["similar_logs"]) >= 1


def test_severity_assessment_critical(service, repo):
    """测试严重程度评估 - CRITICAL"""
    log = repo.create({
        "content": "Critical error",
        "exception_type": "DatabaseError",
        "severity": "CRITICAL",
    })

    result = service.diagnose(log["id"])
    assert result["severity_assessment"] == "CRITICAL"
