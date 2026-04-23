# tests/unit/test_repository.py
"""Mock Repository 测试"""
import pytest
from datetime import datetime, timedelta
from backend.repository.mock import MockRepository


@pytest.fixture
def repo():
    """测试夹具"""
    r = MockRepository()
    yield r
    r.clear()


@pytest.fixture
def sample_logs(repo):
    """创建测试数据"""
    logs = [
        {"content": "Log 1", "exception_type": "NullPointerException", "severity": "HIGH", "service_name": "user-service"},
        {"content": "Log 2", "exception_type": "TimeoutError", "severity": "CRITICAL", "service_name": "order-service"},
        {"content": "Log 3", "exception_type": "DatabaseError", "severity": "MEDIUM", "service_name": "user-service"},
        {"content": "Search me", "exception_type": "Other", "severity": "LOW", "service_name": "auth-service"},
    ]
    created = []
    for log in logs:
        created.append(repo.create(log))
    return created


def test_create_log(repo):
    """测试创建日志"""
    log = repo.create({
        "content": "Test log",
        "exception_type": "Other",
        "severity": "LOW"
    })
    assert log["id"] is not None
    assert log["content"] == "Test log"
    assert log["created_at"] is not None


def test_get_log(repo, sample_logs):
    """测试获取单条日志"""
    log_id = sample_logs[0]["id"]
    retrieved = repo.get(log_id)
    assert retrieved is not None
    assert retrieved["content"] == "Log 1"


def test_get_not_found(repo):
    """测试获取不存在的日志"""
    result = repo.get("non-existent-id")
    assert result is None


def test_get_all_pagination(repo, sample_logs):
    """测试分页"""
    result = repo.get_all(page=1, page_size=2)
    assert result["total"] == 4
    assert result["page"] == 1
    assert result["page_size"] == 2
    assert result["total_pages"] == 2
    assert len(result["items"]) == 2


def test_filter_by_exception_type(repo, sample_logs):
    """测试按异常类型筛选"""
    result = repo.get_all(exception_type="NullPointerException")
    assert result["total"] == 1
    assert result["items"][0]["exception_type"] == "NullPointerException"


def test_filter_by_severity(repo, sample_logs):
    """测试按严重程度筛选"""
    result = repo.get_all(severity="HIGH")
    assert result["total"] == 1


def test_filter_by_service(repo, sample_logs):
    """测试按服务名筛选"""
    result = repo.get_all(service_name="user-service")
    assert result["total"] == 2


def test_search(repo, sample_logs):
    """测试搜索"""
    result = repo.get_all(search="Search me")
    assert result["total"] == 1


def test_update(repo, sample_logs):
    """测试更新"""
    log_id = sample_logs[0]["id"]
    updated = repo.update(log_id, {"severity": "CRITICAL"})
    assert updated is not None
    assert updated["severity"] == "CRITICAL"


def test_update_not_found(repo):
    """测试更新不存在的日志"""
    result = repo.update("non-existent", {"severity": "HIGH"})
    assert result is None


def test_delete(repo, sample_logs):
    """测试删除"""
    log_id = sample_logs[0]["id"]
    result = repo.delete(log_id)
    assert result is True
    assert repo.get(log_id) is None


def test_delete_batch(repo, sample_logs):
    """测试批量删除"""
    ids = [log["id"] for log in sample_logs[:2]]
    count = repo.delete_batch(ids)
    assert count == 2
    assert repo.get_all()["total"] == 2


def test_get_stats(repo, sample_logs):
    """测试统计数据"""
    stats = repo.get_stats()
    assert "exception_type_distribution" in stats
    assert "severity_distribution" in stats
    assert "trend" in stats
    assert "top_services" in stats
    assert len(stats["top_services"]) > 0
