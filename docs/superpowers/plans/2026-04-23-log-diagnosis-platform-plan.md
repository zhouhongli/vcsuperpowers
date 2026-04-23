# 智能日志分析与诊断平台 - 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 开发一个完整的智能日志分析与诊断平台，包含前端表单提交、日志 CRUD、可视化仪表盘和一键诊断功能。

**Architecture:** 前后端分离架构，前端使用 Bootstrap 5 静态页面，后端使用 FastAPI 提供 REST API，数据层使用 Mock Repository 模式预留数据库接口。

**Tech Stack:** 
- Frontend: HTML5/CSS3/JavaScript ES6 + Bootstrap 5.3 + Chart.js 4.x
- Backend: Python 3.11 + FastAPI + Uvicorn
- Testing: pytest + httpx TestClient
- Deployment: Docker 24.x + docker-compose

---

## 任务总览

| 迭代 | 任务范围 | 预计 Task 数 |
|------|----------|-------------|
| 迭代 1 | 项目 Scaffold + 数据模型 + Mock Repository | Task 1-10 |
| 迭代 2 | FastAPI 基础 API（日志 CRUD） | Task 11-20 |
| 迭代 3 | 诊断引擎（规则匹配） | Task 21-28 |
| 迭代 4 | 前端基础（布局 + 表单提交） | Task 29-36 |
| 迭代 5 | 前端列表页 + 详情页 | Task 37-44 |
| 迭代 6 | 仪表盘图表 + 诊断详情页 | Task 45-52 |
| 迭代 7 | Docker 配置 + 集成测试 | Task 53-60 |

---

## 迭代 1: 项目 Scaffold + 数据模型 + Mock Repository

### Task 1: 创建项目根目录结构

**Files:**
- Create: `backend/__init__.py`
- Create: `backend/models/__init__.py`
- Create: `backend/schemas/__init__.py`
- Create: `backend/repository/__init__.py`
- Create: `backend/services/__init__.py`
- Create: `backend/utils/__init__.py`
- Create: `frontend/css/__init__.py`
- Create: `frontend/js/__init__.py`
- Create: `tests/__init__.py`
- Create: `tests/unit/__init__.py`
- Create: `tests/integration/__init__.py`

- [ ] **Step 1: 创建目录和空包文件**

```bash
mkdir -p backend/models backend/schemas backend/repository backend/services backend/utils
mkdir -p frontend/css frontend/js
mkdir -p tests/unit tests/integration
```

```bash
touch backend/__init__.py backend/models/__init__.py backend/schemas/__init__.py
touch backend/repository/__init__.py backend/services/__init__.py backend/utils/__init__.py
touch frontend/css/__init__.py frontend/js/__init__.py
touch tests/__init__.py tests/unit/__init__.py tests/integration/__init__.py
```

- [ ] **Step 2: 验证目录结构**

```bash
tree -L 3 -I '__pycache__|*.pyc'
```

预期输出包含所有上述目录和 `__init__.py` 文件。

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "feat: initial project structure"
```

---

### Task 2: 创建 requirements.txt

**Files:**
- Create: `requirements.txt`

- [ ] **Step 1: 创建依赖文件**

```txt
# requirements.txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
python-multipart==0.0.6
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0
```

- [ ] **Step 2: 创建 .gitignore**

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv

# pytest
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

- [ ] **Step 3: Commit**

```bash
git add requirements.txt .gitignore
git commit -m "chore: add Python dependencies and gitignore"
```

---

### Task 3: 创建日志数据模型 (LogEntry)

**Files:**
- Create: `backend/models/log_entry.py`

- [ ] **Step 1: 编写数据模型定义**

```python
# backend/models/log_entry.py
"""日志条目数据模型"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum
import uuid


class ExceptionType(str, Enum):
    """异常类型枚举"""
    NULL_POINTER = "NullPointerException"
    TIMEOUT = "TimeoutError"
    DATABASE = "DatabaseError"
    AUTHENTICATION = "AuthenticationError"
    OTHER = "Other"


class SeverityLevel(str, Enum):
    """严重程度枚举"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class LogEntry:
    """日志条目"""
    content: str
    exception_type: str
    severity: str
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    occurred_at: Optional[datetime] = None
    service_name: Optional[str] = None
    stack_trace: Optional[str] = None
    user_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "content": self.content,
            "exception_type": self.exception_type,
            "severity": self.severity,
            "occurred_at": self.occurred_at.isoformat() if self.occurred_at else None,
            "service_name": self.service_name,
            "stack_trace": self.stack_trace,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "LogEntry":
        """从字典创建"""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            content=data["content"],
            exception_type=data["exception_type"],
            severity=data["severity"],
            occurred_at=datetime.fromisoformat(data["occurred_at"]) if data.get("occurred_at") else None,
            service_name=data.get("service_name"),
            stack_trace=data.get("stack_trace"),
            user_id=data.get("user_id"),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.now(),
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else datetime.now(),
        )
```

- [ ] **Step 2: 更新 models/__init__.py**

```python
# backend/models/__init__.py
from .log_entry import LogEntry, ExceptionType, SeverityLevel

__all__ = ["LogEntry", "ExceptionType", "SeverityLevel"]
```

- [ ] **Step 3: 编写单元测试**

```python
# tests/unit/test_log_entry.py
"""LogEntry 数据模型测试"""
import pytest
from datetime import datetime
from backend.models.log_entry import LogEntry, ExceptionType, SeverityLevel


def test_create_log_entry_minimal():
    """测试创建最小化日志条目"""
    log = LogEntry(
        content="Test log content",
        exception_type="NullPointerException",
        severity="HIGH"
    )
    assert log.id is not None
    assert log.content == "Test log content"
    assert log.exception_type == "NullPointerException"
    assert log.severity == "HIGH"
    assert log.created_at is not None


def test_create_log_entry_full():
    """测试创建完整日志条目"""
    log = LogEntry(
        content="Test log",
        exception_type="TimeoutError",
        severity="CRITICAL",
        occurred_at=datetime(2026, 4, 23, 10, 0),
        service_name="user-service",
        stack_trace="at com.example.Service.method(Service.java:42)",
        user_id="user-123"
    )
    assert log.service_name == "user-service"
    assert log.stack_trace is not None
    assert log.user_id == "user-123"


def test_log_entry_to_dict():
    """测试 to_dict 方法"""
    log = LogEntry(
        content="Test",
        exception_type="Other",
        severity="LOW"
    )
    data = log.to_dict()
    assert data["id"] == log.id
    assert data["content"] == "Test"
    assert data["severity"] == "LOW"
    assert "created_at" in data


def test_log_entry_from_dict():
    """测试 from_dict 方法"""
    data = {
        "id": "test-id",
        "content": "Test content",
        "exception_type": "DatabaseError",
        "severity": "MEDIUM",
        "service_name": "order-service"
    }
    log = LogEntry.from_dict(data)
    assert log.id == "test-id"
    assert log.content == "Test content"
    assert log.service_name == "order-service"
```

- [ ] **Step 4: 运行测试**

```bash
pytest tests/unit/test_log_entry.py -v
```
预期：4 个测试全部 PASS

- [ ] **Step 5: Commit**

```bash
git add backend/models/log_entry.py backend/models/__init__.py tests/unit/test_log_entry.py
git commit -m "feat: add LogEntry data model with unit tests"
```

---

### Task 4: 创建 Pydantic Schemas（请求/响应模型）

**Files:**
- Create: `backend/schemas/log_schemas.py`

- [ ] **Step 1: 创建 Pydantic 模型**

```python
# backend/schemas/log_schemas.py
"""Pydantic 请求/响应模型"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from enum import Enum


class ExceptionTypeEnum(str, Enum):
    """异常类型"""
    NULL_POINTER = "NullPointerException"
    TIMEOUT = "TimeoutError"
    DATABASE = "DatabaseError"
    AUTHENTICATION = "AuthenticationError"
    OTHER = "Other"


class SeverityEnum(str, Enum):
    """严重程度"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class LogCreate(BaseModel):
    """创建日志请求体"""
    content: str = Field(..., min_length=1, description="日志内容")
    exception_type: ExceptionTypeEnum = Field(..., description="异常类型")
    severity: SeverityEnum = Field(..., description="严重程度")
    occurred_at: Optional[datetime] = Field(None, description="发生时间")
    service_name: Optional[str] = Field(None, description="服务名称")
    stack_trace: Optional[str] = Field(None, description="堆栈跟踪")
    user_id: Optional[str] = Field(None, description="用户 ID")


class LogUpdate(BaseModel):
    """更新日志请求体"""
    content: Optional[str] = Field(None, min_length=1, description="日志内容")
    exception_type: Optional[ExceptionTypeEnum] = Field(None, description="异常类型")
    severity: Optional[SeverityEnum] = Field(None, description="严重程度")
    occurred_at: Optional[datetime] = Field(None, description="发生时间")
    service_name: Optional[str] = Field(None, description="服务名称")
    stack_trace: Optional[str] = Field(None, description="堆栈跟踪")
    user_id: Optional[str] = Field(None, description="用户 ID")


class LogResponse(BaseModel):
    """日志响应体"""
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    content: str
    exception_type: str
    severity: str
    occurred_at: Optional[datetime]
    service_name: Optional[str]
    stack_trace: Optional[str]
    user_id: Optional[str]
    created_at: datetime
    updated_at: datetime


class LogListResponse(BaseModel):
    """日志列表响应体"""
    items: List[LogResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class BatchDeleteRequest(BaseModel):
    """批量删除请求体"""
    ids: List[str]
```

- [ ] **Step 2: 更新 schemas/__init__.py**

```python
# backend/schemas/__init__.py
from .log_schemas import (
    LogCreate,
    LogUpdate,
    LogResponse,
    LogListResponse,
    BatchDeleteRequest,
    ExceptionTypeEnum,
    SeverityEnum,
)

__all__ = [
    "LogCreate",
    "LogUpdate",
    "LogResponse",
    "LogListResponse",
    "BatchDeleteRequest",
    "ExceptionTypeEnum",
    "SeverityEnum",
]
```

- [ ] **Step 3: Commit**

```bash
git add backend/schemas/log_schemas.py backend/schemas/__init__.py
git commit -m "feat: add Pydantic schemas for API request/response"
```

---

### Task 5: 创建 Repository 基类（接口定义）

**Files:**
- Create: `backend/repository/base.py`

- [ ] **Step 1: 定义 Repository 抽象基类**

```python
# backend/repository/base.py
"""Repository 抽象基类 - 定义数据访问层接口"""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime


class RepositoryBase(ABC):
    """Repository 基类"""
    
    @abstractmethod
    def get(self, id: str) -> Optional[Dict[str, Any]]:
        """获取单条日志"""
        pass
    
    @abstractmethod
    def get_all(
        self,
        page: int = 1,
        page_size: int = 10,
        exception_type: Optional[str] = None,
        severity: Optional[str] = None,
        service_name: Optional[str] = None,
        search: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """获取日志列表（分页、筛选）"""
        pass
    
    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """创建日志"""
        pass
    
    @abstractmethod
    def update(self, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新日志"""
        pass
    
    @abstractmethod
    def delete(self, id: str) -> bool:
        """删除日志"""
        pass
    
    @abstractmethod
    def delete_batch(self, ids: List[str]) -> int:
        """批量删除日志"""
        pass
    
    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """获取仪表盘统计数据"""
        pass
```

- [ ] **Step 2: 更新 repository/__init__.py**

```python
# backend/repository/__init__.py
from .base import RepositoryBase

__all__ = ["RepositoryBase"]
```

- [ ] **Step 3: Commit**

```bash
git add backend/repository/base.py backend/repository/__init__.py
git commit -m "feat: define Repository abstract base class"
```

---

### Task 6: 创建 Mock Repository 实现

**Files:**
- Create: `backend/repository/mock.py`

- [ ] **Step 1: 实现 Mock Repository**

```python
# backend/repository/mock.py
"""Mock Repository 实现 - 内存存储"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from .base import RepositoryBase
from ..models.log_entry import LogEntry
import uuid


class MockRepository(RepositoryBase):
    """Mock Repository - 内存存储实现"""
    
    def __init__(self):
        self._storage: Dict[str, Dict[str, Any]] = {}
    
    def get(self, id: str) -> Optional[Dict[str, Any]]:
        """获取单条日志"""
        return self._storage.get(id)
    
    def get_all(
        self,
        page: int = 1,
        page_size: int = 10,
        exception_type: Optional[str] = None,
        severity: Optional[str] = None,
        service_name: Optional[str] = None,
        search: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """获取日志列表（分页、筛选）"""
        items = list(self._storage.values())
        
        # 筛选
        if exception_type:
            items = [i for i in items if i["exception_type"] == exception_type]
        if severity:
            items = [i for i in items if i["severity"] == severity]
        if service_name:
            items = [i for i in items if i.get("service_name") == service_name]
        if search:
            search_lower = search.lower()
            items = [
                i for i in items
                if search_lower in i["content"].lower()
                or (i.get("service_name") and search_lower in i["service_name"].lower())
                or (i.get("user_id") and search_lower in i["user_id"].lower())
            ]
        if date_from:
            items = [i for i in items if i.get("occurred_at") and datetime.fromisoformat(i["occurred_at"]) >= date_from]
        if date_to:
            items = [i for i in items if i.get("occurred_at") and datetime.fromisoformat(i["occurred_at"]) <= date_to]
        
        # 按时间倒序
        items.sort(key=lambda x: x["created_at"], reverse=True)
        
        # 分页
        total = len(items)
        total_pages = (total + page_size - 1) // page_size
        start = (page - 1) * page_size
        end = start + page_size
        paginated = items[start:end]
        
        return {
            "items": paginated,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """创建日志"""
        log_id = data.get("id", str(uuid.uuid4()))
        now = datetime.now().isoformat()
        
        log_data = {
            "id": log_id,
            "content": data["content"],
            "exception_type": data["exception_type"],
            "severity": data["severity"],
            "occurred_at": data.get("occurred_at"),
            "service_name": data.get("service_name"),
            "stack_trace": data.get("stack_trace"),
            "user_id": data.get("user_id"),
            "created_at": now,
            "updated_at": now,
        }
        
        self._storage[log_id] = log_data
        return log_data
    
    def update(self, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新日志"""
        if id not in self._storage:
            return None
        
        existing = self._storage[id]
        for key, value in data.items():
            if value is not None:
                existing[key] = value
        existing["updated_at"] = datetime.now().isoformat()
        
        return existing
    
    def delete(self, id: str) -> bool:
        """删除日志"""
        if id in self._storage:
            del self._storage[id]
            return True
        return False
    
    def delete_batch(self, ids: List[str]) -> int:
        """批量删除日志"""
        count = 0
        for id in ids:
            if self.delete(id):
                count += 1
        return count
    
    def get_stats(self) -> Dict[str, Any]:
        """获取仪表盘统计数据"""
        items = list(self._storage.values())
        
        # 异常类型分布
        exception_distribution: Dict[str, int] = {}
        for item in items:
            exc_type = item["exception_type"]
            exception_distribution[exc_type] = exception_distribution.get(exc_type, 0) + 1
        
        # 严重程度分布
        severity_distribution: Dict[str, int] = {}
        for item in items:
            sev = item["severity"]
            severity_distribution[sev] = severity_distribution.get(sev, 0) + 1
        
        # 服务排名
        service_counts: Dict[str, int] = {}
        for item in items:
            service = item.get("service_name")
            if service:
                service_counts[service] = service_counts.get(service, 0) + 1
        top_services = sorted(service_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # 趋势（近 7 天）
        from datetime import timedelta
        today = datetime.now().date()
        trend: List[Dict[str, Any]] = []
        for i in range(7):
            date = today - timedelta(days=6-i)
            date_str = date.isoformat()
            count = sum(
                1 for item in items
                if item.get("occurred_at")
                and datetime.fromisoformat(item["occurred_at"]).date() == date
            )
            trend.append({"date": date_str, "count": count})
        
        return {
            "exception_type_distribution": [
                {"type": k, "count": v} for k, v in exception_distribution.items()
            ],
            "severity_distribution": [
                {"level": k, "count": v} for k, v in severity_distribution.items()
            ],
            "trend": trend,
            "top_services": [{"service": k, "count": v} for k, v in top_services],
        }
    
    def clear(self):
        """清空所有数据（测试用）"""
        self._storage.clear()
```

- [ ] **Step 2: 更新 repository/__init__.py**

```python
# backend/repository/__init__.py
from .base import RepositoryBase
from .mock import MockRepository

__all__ = ["RepositoryBase", "MockRepository"]
```

- [ ] **Step 3: 编写单元测试**

```python
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
```

- [ ] **Step 4: 运行测试**

```bash
pytest tests/unit/test_repository.py -v
```
预期：15 个测试全部 PASS

- [ ] **Step 5: Commit**

```bash
git add backend/repository/mock.py backend/repository/__init__.py tests/unit/test_repository.py
git commit -m "feat: implement Mock Repository with comprehensive unit tests"
```

---

### Task 7: 创建诊断结果数据模型

**Files:**
- Create: `backend/models/diagnosis.py`

- [ ] **Step 1: 创建诊断模型**

```python
# backend/models/diagnosis.py
"""诊断结果数据模型"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import uuid


@dataclass
class Diagnosis:
    """诊断结果"""
    log_id: str
    root_cause: str
    solution: str
    severity_assessment: str
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    similar_logs: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "log_id": self.log_id,
            "root_cause": self.root_cause,
            "solution": self.solution,
            "severity_assessment": self.severity_assessment,
            "similar_logs": self.similar_logs,
            "created_at": self.created_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Diagnosis":
        """从字典创建"""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            log_id=data["log_id"],
            root_cause=data["root_cause"],
            solution=data["solution"],
            severity_assessment=data["severity_assessment"],
            similar_logs=data.get("similar_logs", []),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.now(),
        )
```

- [ ] **Step 2: 更新 models/__init__.py**

```python
# backend/models/__init__.py
from .log_entry import LogEntry, ExceptionType, SeverityLevel
from .diagnosis import Diagnosis

__all__ = ["LogEntry", "ExceptionType", "SeverityLevel", "Diagnosis"]
```

- [ ] **Step 3: Commit**

```bash
git add backend/models/diagnosis.py backend/models/__init__.py
git commit -m "feat: add Diagnosis data model"
```

---

### Task 8: 创建诊断 Pydantic Schema

**Files:**
- Create: `backend/schemas/diagnosis_schemas.py`

- [ ] **Step 1: 创建诊断 Schema**

```python
# backend/schemas/diagnosis_schemas.py
"""诊断相关 Pydantic 模型"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class DiagnosisResponse(BaseModel):
    """诊断结果响应体"""
    id: str
    log_id: str
    root_cause: str
    solution: str
    severity_assessment: str
    similar_logs: List[str]
    created_at: datetime


class DiagnosisCreateRequest(BaseModel):
    """创建诊断请求体（用于大模型降级）"""
    content: str
    exception_type: str
    severity: str
    service_name: Optional[str] = None
    stack_trace: Optional[str] = None
```

- [ ] **Step 2: 更新 schemas/__init__.py**

```python
# backend/schemas/__init__.py
from .log_schemas import (
    LogCreate,
    LogUpdate,
    LogResponse,
    LogListResponse,
    BatchDeleteRequest,
    ExceptionTypeEnum,
    SeverityEnum,
)
from .diagnosis_schemas import (
    DiagnosisResponse,
    DiagnosisCreateRequest,
)

__all__ = [
    "LogCreate",
    "LogUpdate",
    "LogResponse",
    "LogListResponse",
    "BatchDeleteRequest",
    "ExceptionTypeEnum",
    "SeverityEnum",
    "DiagnosisResponse",
    "DiagnosisCreateRequest",
]
```

- [ ] **Step 3: Commit**

```bash
git add backend/schemas/diagnosis_schemas.py backend/schemas/__init__.py
git commit -m "feat: add Pydantic schemas for diagnosis"
```

---

### Task 9: 创建自定义异常类

**Files:**
- Create: `backend/utils/exceptions.py`

- [ ] **Step 1: 定义异常类**

```python
# backend/utils/exceptions.py
"""自定义异常类"""


class LogNotFoundError(Exception):
    """日志不存在"""
    status_code = 404
    error_code = "LOG_NOT_FOUND"
    
    def __init__(self, log_id: str):
        self.log_id = log_id
        super().__init__(f"Log with ID '{log_id}' not found")


class InvalidLogDataError(Exception):
    """日志数据格式错误"""
    status_code = 400
    error_code = "INVALID_LOG_DATA"
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class DiagnosisNotFoundError(Exception):
    """诊断结果不存在"""
    status_code = 404
    error_code = "DIAGNOSIS_NOT_FOUND"
    
    def __init__(self, diagnosis_id: str):
        self.diagnosis_id = diagnosis_id
        super().__init__(f"Diagnosis with ID '{diagnosis_id}' not found")


class DiagnosisAlreadyExistsError(Exception):
    """诊断结果已存在"""
    status_code = 409
    error_code = "DIAGNOSIS_ALREADY_EXISTS"
    
    def __init__(self, log_id: str):
        self.log_id = log_id
        super().__init__(f"Diagnosis already exists for log '{log_id}'")
```

- [ ] **Step 2: 更新 utils/__init__.py**

```python
# backend/utils/__init__.py
from .exceptions import (
    LogNotFoundError,
    InvalidLogDataError,
    DiagnosisNotFoundError,
    DiagnosisAlreadyExistsError,
)

__all__ = [
    "LogNotFoundError",
    "InvalidLogDataError",
    "DiagnosisNotFoundError",
    "DiagnosisAlreadyExistsError",
]
```

- [ ] **Step 3: Commit**

```bash
git add backend/utils/exceptions.py backend/utils/__init__.py
git commit -m "feat: add custom exception classes"
```

---

### Task 10: 创建 FastAPI 主应用入口

**Files:**
- Create: `backend/main.py`

- [ ] **Step 1: 创建 FastAPI 应用**

```python
# backend/main.py
"""FastAPI 应用入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .repository.mock import MockRepository
from .services.diagnosis import DiagnosisService

app = FastAPI(
    title="智能日志分析与诊断平台",
    description="提供日志提交、管理、可视化仪表盘和一键诊断功能",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境，生产环境需限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局 Repository 实例
repository = MockRepository()

# 全局诊断服务实例
diagnosis_service = DiagnosisService(repository)


@app.get("/")
def root():
    """根路径"""
    return {"message": "智能日志分析与诊断平台 API", "docs": "/docs"}


@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "healthy"}


# 导入路由
from .routes import logs, diagnosis, dashboard

app.include_router(logs.router, prefix="/api", tags=["logs"])
app.include_router(diagnosis.router, prefix="/api", tags=["diagnosis"])
app.include_router(dashboard.router, prefix="/api", tags=["dashboard"])
```

- [ ] **Step 2: 创建路由目录和基础文件**

```python
# backend/routes/__init__.py
from . import logs
from . import diagnosis
from . import dashboard

__all__ = ["logs", "diagnosis", "dashboard"]
```

- [ ] **Step 3: 验证应用可启动**

```bash
cd backend
python -c "from main import app; print('App loaded successfully')"
```

- [ ] **Step 4: Commit**

```bash
git add backend/main.py backend/routes/__init__.py
git commit -m "feat: create FastAPI application entry point"
```

---

## 迭代 2: FastAPI 基础 API（日志 CRUD）

### Task 11: 创建日志路由 - 创建和查询

**Files:**
- Create: `backend/routes/logs.py`

- [ ] **Step 1: 实现 POST /api/logs 和 GET /api/logs**

```python
# backend/routes/logs.py
"""日志管理路由"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from datetime import datetime

from backend.schemas.log_schemas import (
    LogCreate,
    LogResponse,
    LogListResponse,
    BatchDeleteRequest,
)
from backend.repository.mock import MockRepository

router = APIRouter()

# 全局 Repository 实例（从 main 导入）
from backend.main import repository


@router.post("/logs", response_model=LogResponse, status_code=201)
def create_log(log_data: LogCreate):
    """创建日志条目"""
    data = log_data.model_dump()
    # 转换 enum 为字符串
    data["exception_type"] = data["exception_type"].value
    data["severity"] = data["severity"].value
    # 处理 datetime
    if data.get("occurred_at"):
        data["occurred_at"] = data["occurred_at"].isoformat()
    
    created = repository.create(data)
    return LogResponse(**created)


@router.get("/logs", response_model=LogListResponse)
def get_logs(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    exception_type: Optional[str] = Query(None, description="异常类型"),
    severity: Optional[str] = Query(None, description="严重程度"),
    service_name: Optional[str] = Query(None, description="服务名称"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    date_from: Optional[datetime] = Query(None, description="起始日期"),
    date_to: Optional[datetime] = Query(None, description="结束日期"),
):
    """获取日志列表"""
    result = repository.get_all(
        page=page,
        page_size=page_size,
        exception_type=exception_type,
        severity=severity,
        service_name=service_name,
        search=search,
        date_from=date_from,
        date_to=date_to,
    )
    return LogListResponse(**result)
```

- [ ] **Step 2: 编写集成测试**

```python
# tests/integration/test_logs_api.py
"""日志 API 集成测试"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_repository():
    """每个测试前清空仓库"""
    from backend.main import repository
    repository.clear()
    yield


def test_create_log_minimal():
    """测试创建最小化日志"""
    response = client.post(
        "/api/logs",
        json={
            "content": "Test log content",
            "exception_type": "Other",
            "severity": "LOW"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "Test log content"
    assert data["id"] is not None


def test_create_log_full():
    """测试创建完整日志"""
    response = client.post(
        "/api/logs",
        json={
            "content": "Error occurred",
            "exception_type": "NullPointerException",
            "severity": "HIGH",
            "occurred_at": "2026-04-23T10:00:00",
            "service_name": "user-service",
            "stack_trace": "at com.example.Service.method(Service.java:42)",
            "user_id": "user-123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["exception_type"] == "NullPointerException"
    assert data["service_name"] == "user-service"


def test_create_log_invalid_severity():
    """测试无效严重程度"""
    response = client.post(
        "/api/logs",
        json={
            "content": "Test",
            "exception_type": "Other",
            "severity": "INVALID"
        }
    )
    assert response.status_code == 422


def test_get_logs_empty():
    """测试空列表"""
    response = client.get("/api/logs")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


def test_get_logs_with_data():
    """测试获取日志列表"""
    # 先创建数据
    client.post("/api/logs", json={"content": "Log 1", "exception_type": "Other", "severity": "LOW"})
    client.post("/api/logs", json={"content": "Log 2", "exception_type": "TimeoutError", "severity": "HIGH"})
    
    response = client.get("/api/logs")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_get_logs_pagination():
    """测试分页"""
    for i in range(25):
        client.post("/api/logs", json={"content": f"Log {i}", "exception_type": "Other", "severity": "LOW"})
    
    response = client.get("/api/logs?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 25
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert len(data["items"]) == 10


def test_filter_by_exception_type():
    """测试按异常类型筛选"""
    client.post("/api/logs", json={"content": "Log 1", "exception_type": "NullPointerException", "severity": "HIGH"})
    client.post("/api/logs", json={"content": "Log 2", "exception_type": "TimeoutError", "severity": "HIGH"})
    
    response = client.get("/api/logs?exception_type=NullPointerException")
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["exception_type"] == "NullPointerException"


def test_filter_by_severity():
    """测试按严重程度筛选"""
    client.post("/api/logs", json={"content": "Log 1", "exception_type": "Other", "severity": "HIGH"})
    client.post("/api/logs", json={"content": "Log 2", "exception_type": "Other", "severity": "LOW"})
    
    response = client.get("/api/logs?severity=HIGH")
    data = response.json()
    assert data["total"] == 1


def test_search():
    """测试搜索"""
    client.post("/api/logs", json={"content": "Search for this unique text", "exception_type": "Other", "severity": "LOW"})
    
    response = client.get("/api/logs?search=unique")
    data = response.json()
    assert data["total"] == 1
```

- [ ] **Step 3: 运行测试**

```bash
pytest tests/integration/test_logs_api.py -v
```
预期：9 个测试全部 PASS

- [ ] **Step 4: Commit**

```bash
git add backend/routes/logs.py tests/integration/test_logs_api.py
git commit -m "feat: implement create and list logs API endpoints"
```

---

### Task 12: 创建日志路由 - 详情、更新和删除

**Files:**
- Modify: `backend/routes/logs.py:50-end`

- [ ] **Step 1: 添加 GET/PUT/DELETE /api/logs/{id}**

```python
# 添加到 backend/routes/logs.py 文件末尾

@router.get("/logs/{log_id}", response_model=LogResponse)
def get_log(log_id: str):
    """获取单条日志详情"""
    log = repository.get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail=f"Log with ID '{log_id}' not found")
    return LogResponse(**log)


@router.put("/logs/{log_id}", response_model=LogResponse)
def update_log(log_id: str, log_data: dict):
    """更新日志"""
    existing = repository.get(log_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Log with ID '{log_id}' not found")
    
    # 只更新提供的字段
    update_data = {k: v for k, v in log_data.items() if v is not None}
    
    # 处理 enum
    if "exception_type" in update_data:
        update_data["exception_type"] = str(update_data["exception_type"])
    if "severity" in update_data:
        update_data["severity"] = str(update_data["severity"])
    
    updated = repository.update(log_id, update_data)
    return LogResponse(**updated)


@router.delete("/logs/{log_id}", status_code=204)
def delete_log(log_id: str):
    """删除单条日志"""
    if not repository.delete(log_id):
        raise HTTPException(status_code=404, detail=f"Log with ID '{log_id}' not found")
    return None


@router.delete("/logs", status_code=204)
def delete_logs_batch(request: BatchDeleteRequest):
    """批量删除日志"""
    repository.delete_batch(request.ids)
    return None
```

- [ ] **Step 2: 添加集成测试**

```python
# 添加到 tests/integration/test_logs_api.py

def test_get_log_detail():
    """测试获取日志详情"""
    create_response = client.post("/api/logs", json={
        "content": "Detail test",
        "exception_type": "Other",
        "severity": "MEDIUM"
    })
    log_id = create_response.json()["id"]
    
    response = client.get(f"/api/logs/{log_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Detail test"


def test_get_log_not_found():
    """测试获取不存在的日志"""
    response = client.get("/api/logs/non-existent-id")
    assert response.status_code == 404


def test_update_log():
    """测试更新日志"""
    create_response = client.post("/api/logs", json={
        "content": "Original",
        "exception_type": "Other",
        "severity": "LOW"
    })
    log_id = create_response.json()["id"]
    
    response = client.put(f"/api/logs/{log_id}", json={
        "content": "Updated content",
        "severity": "HIGH"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Updated content"
    assert data["severity"] == "HIGH"


def test_update_not_found():
    """测试更新不存在的日志"""
    response = client.put("/api/logs/non-existent", json={"content": "Test"})
    assert response.status_code == 404


def test_delete_log():
    """测试删除日志"""
    create_response = client.post("/api/logs", json={
        "content": "To delete",
        "exception_type": "Other",
        "severity": "LOW"
    })
    log_id = create_response.json()["id"]
    
    response = client.delete(f"/api/logs/{log_id}")
    assert response.status_code == 204
    
    # 验证已删除
    get_response = client.get(f"/api/logs/{log_id}")
    assert get_response.status_code == 404


def test_delete_not_found():
    """测试删除不存在的日志"""
    response = client.delete("/api/logs/non-existent")
    assert response.status_code == 404


def test_batch_delete():
    """测试批量删除"""
    ids = []
    for i in range(3):
        create_response = client.post("/api/logs", json={
            "content": f"Batch {i}",
            "exception_type": "Other",
            "severity": "LOW"
        })
        ids.append(create_response.json()["id"])
    
    response = client.request("DELETE", "/api/logs", json={"ids": ids})
    assert response.status_code == 204
    
    # 验证已删除
    list_response = client.get("/api/logs")
    assert list_response.json()["total"] == 0
```

- [ ] **Step 3: 运行所有日志测试**

```bash
pytest tests/integration/test_logs_api.py -v
```
预期：16 个测试全部 PASS

- [ ] **Step 4: Commit**

```bash
git add backend/routes/logs.py tests/integration/test_logs_api.py
git commit -m "feat: implement get, update, delete log API endpoints"
```

---

## 迭代 3: 诊断引擎（规则匹配）

### Task 21: 创建诊断规则库

**Files:**
- Create: `backend/services/diagnosis_rules.py`

- [ ] **Step 1: 定义诊断规则**

```python
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
```

- [ ] **Step 2: 编写单元测试**

```python
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
    assert "null" in matched or "getinstance()" in matched


def test_match_timeout_with_database():
    """测试 TimeoutError 数据库场景"""
    content = "Database query timeout after 30s"
    
    score, rule, matched = match_rule("TimeoutError", content)
    
    assert score >= 0.8
    assert "database" in matched


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
    
    assert "null" in matched
```

- [ ] **Step 3: 运行测试**

```bash
pytest tests/unit/test_diagnosis_rules.py -v
```
预期：5 个测试全部 PASS

- [ ] **Step 4: Commit**

```bash
git add backend/services/diagnosis_rules.py tests/unit/test_diagnosis_rules.py
git commit -m "feat: create diagnosis rule base with keyword matching"
```

---

### Task 22: 创建诊断服务（规则引擎）

**Files:**
- Create: `backend/services/diagnosis.py`

- [ ] **Step 1: 实现诊断服务**

```python
# backend/services/diagnosis.py
"""诊断服务"""
from typing import Dict, Any, List, Optional
from datetime import datetime

from .diagnosis_rules import match_rule
from ..models.diagnosis import Diagnosis
from ..repository.mock import MockRepository


class DiagnosisService:
    """诊断服务"""
    
    def __init__(self, repository: MockRepository):
        self.repository = repository
        self._diagnoses: Dict[str, Dict[str, Any]] = {}
    
    def diagnose(self, log_id: str) -> Dict[str, Any]:
        """
        诊断指定日志
        
        Args:
            log_id: 日志 ID
            
        Returns:
            诊断结果
        """
        # 获取日志
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
        
        # 构建根因分析
        matched_info = f"匹配到关键词：{', '.join(matched_keywords)}" if matched_keywords else "未匹配到特定关键词"
        root_cause = rule["root_cause_template"].format(matched_info=matched_info)
        
        # 查找相似日志
        similar_logs = self._find_similar_logs(log, exclude_id=log_id, limit=3)
        
        # 创建诊断结果
        diagnosis = Diagnosis(
            log_id=log_id,
            root_cause=root_cause,
            solution="\n".join(f"{i+1}. {s}" for i, s in enumerate(rule["solutions"])),
            severity_assessment=self._assess_severity(log["severity"], score),
            similar_logs=similar_logs,
        )
        
        diagnosis_data = diagnosis.to_dict()
        diagnosis_data["confidence"] = score
        diagnosis_data["matched_keywords"] = matched_keywords
        
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
```

- [ ] **Step 2: 编写单元测试**

```python
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
```

- [ ] **Step 3: 运行测试**

```bash
pytest tests/unit/test_diagnosis_service.py -v
```
预期：7 个测试全部 PASS

- [ ] **Step 4: Commit**

```bash
git add backend/services/diagnosis.py tests/unit/test_diagnosis_service.py
git commit -m "feat: implement DiagnosisService with rule-based engine"
```

---

### Task 23: 创建诊断路由

**Files:**
- Create: `backend/routes/diagnosis.py`

- [ ] **Step 1: 实现诊断路由**

```python
# backend/routes/diagnosis.py
"""诊断路由"""
from fastapi import APIRouter, HTTPException

from backend.schemas.diagnosis_schemas import DiagnosisResponse
from backend.main import diagnosis_service, repository

router = APIRouter()


@router.post("/logs/{log_id}/diagnose", response_model=DiagnosisResponse)
def create_diagnosis(log_id: str):
    """创建/获取诊断结果"""
    # 检查日志是否存在
    log = repository.get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail=f"Log with ID '{log_id}' not found")
    
    try:
        result = diagnosis_service.diagnose(log_id)
        return DiagnosisResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/logs/{log_id}/diagnosis", response_model=DiagnosisResponse)
def get_diagnosis(log_id: str):
    """获取诊断结果"""
    # 检查日志是否存在
    log = repository.get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail=f"Log with ID '{log_id}' not found")
    
    result = diagnosis_service.get_diagnosis(log_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"No diagnosis found for log '{log_id}'")
    
    return DiagnosisResponse(**result)
```

- [ ] **Step 2: 更新 routes/__init__.py**

```python
# backend/routes/__init__.py
from . import logs
from . import diagnosis
from . import dashboard

__all__ = ["logs", "diagnosis", "dashboard"]
```

- [ ] **Step 3: 编写集成测试**

```python
# tests/integration/test_diagnosis_api.py
"""诊断 API 集成测试"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_repository():
    """每个测试前清空仓库"""
    from backend.main import repository
    repository.clear()
    yield


def test_create_diagnosis():
    """测试创建诊断"""
    # 先创建日志
    create_log = client.post("/api/logs", json={
        "content": "Null pointer at getInstance()",
        "exception_type": "NullPointerException",
        "severity": "HIGH",
        "stack_trace": "at Service.getInstance(Service.java:42)"
    })
    log_id = create_log.json()["id"]
    
    # 创建诊断
    response = client.post(f"/api/logs/{log_id}/diagnose")
    assert response.status_code == 200
    data = response.json()
    assert "root_cause" in data
    assert "solution" in data
    assert data["severity_assessment"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]


def test_create_diagnosis_log_not_found():
    """测试诊断不存在的日志"""
    response = client.post("/api/logs/non-existent/diagnose")
    assert response.status_code == 404


def test_get_diagnosis():
    """测试获取诊断结果"""
    # 先创建日志并诊断
    create_log = client.post("/api/logs", json={
        "content": "Test log",
        "exception_type": "TimeoutError",
        "severity": "CRITICAL"
    })
    log_id = create_log.json()["id"]
    client.post(f"/api/logs/{log_id}/diagnose")
    
    # 获取诊断
    response = client.get(f"/api/logs/{log_id}/diagnosis")
    assert response.status_code == 200
    assert response.json()["log_id"] == log_id


def test_get_diagnosis_not_exists():
    """测试获取不存在的诊断"""
    create_log = client.post("/api/logs", json={
        "content": "Test",
        "exception_type": "Other",
        "severity": "LOW"
    })
    log_id = create_log.json()["id"]
    
    response = client.get(f"/api/logs/{log_id}/diagnosis")
    assert response.status_code == 404
```

- [ ] **Step 4: 运行测试**

```bash
pytest tests/integration/test_diagnosis_api.py -v
```
预期：4 个测试全部 PASS

- [ ] **Step 5: Commit**

```bash
git add backend/routes/diagnosis.py tests/integration/test_diagnosis_api.py
git commit -m "feat: implement diagnosis API endpoints"
```

---

## 迭代 4: 仪表盘 API

### Task 30: 创建仪表盘路由

**Files:**
- Create: `backend/routes/dashboard.py`

- [ ] **Step 1: 实现仪表盘统计 API**

```python
# backend/routes/dashboard.py
"""仪表盘路由"""
from fastapi import APIRouter

from backend.main import repository

router = APIRouter()


@router.get("/dashboard/stats")
def get_dashboard_stats():
    """获取仪表盘统计数据"""
    return repository.get_stats()
```

- [ ] **Step 2: 编写集成测试**

```python
# tests/integration/test_dashboard_api.py
"""仪表盘 API 集成测试"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_repository():
    """清空仓库"""
    from backend.main import repository
    repository.clear()
    yield


@pytest.fixture
def sample_data():
    """创建测试数据"""
    from backend.main import repository
    
    test_logs = [
        {"content": "Log 1", "exception_type": "NullPointerException", "severity": "HIGH", "service_name": "user-service"},
        {"content": "Log 2", "exception_type": "NullPointerException", "severity": "CRITICAL", "service_name": "user-service"},
        {"content": "Log 3", "exception_type": "TimeoutError", "severity": "MEDIUM", "service_name": "order-service"},
        {"content": "Log 4", "exception_type": "DatabaseError", "severity": "LOW", "service_name": "order-service"},
        {"content": "Log 5", "exception_type": "Other", "severity": "LOW", "service_name": "auth-service"},
    ]
    for log in test_logs:
        repository.create(log)


def test_get_stats_empty(client):
    """测试空数据统计"""
    response = client.get("/api/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert "exception_type_distribution" in data
    assert "severity_distribution" in data
    assert "trend" in data
    assert "top_services" in data


def test_get_stats_with_data(client, sample_data):
    """测试有数据时的统计"""
    response = client.get("/api/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    
    # 验证异常类型分布
    assert len(data["exception_type_distribution"]) == 4  # 4 种不同类型
    
    # 验证严重程度分布
    assert len(data["severity_distribution"]) == 4  # LOW, MEDIUM, HIGH, CRITICAL
    
    # 验证 Top 服务
    assert len(data["top_services"]) > 0
    # user-service 应该有 2 条
    user_service = next((s for s in data["top_services"] if s["service"] == "user-service"), None)
    assert user_service is not None
    assert user_service["count"] == 2


def test_trend_data(client, sample_data):
    """测试趋势数据"""
    response = client.get("/api/dashboard/stats")
    data = response.json()
    
    assert len(data["trend"]) == 7  # 近 7 天
    assert "date" in data["trend"][0]
    assert "count" in data["trend"][0]
```

- [ ] **Step 3: 运行测试**

```bash
pytest tests/integration/test_dashboard_api.py -v
```
预期：3 个测试全部 PASS

- [ ] **Step 4: Commit**

```bash
git add backend/routes/dashboard.py tests/integration/test_dashboard_api.py
git commit -m "feat: implement dashboard stats API endpoint"
```

---

## 迭代 5: 前端基础（布局 + 表单提交）

### Task 36: 创建前端首页和导航布局

**Files:**
- Create: `frontend/index.html`
- Create: `frontend/css/style.css`
- Create: `frontend/js/api.js`

- [ ] **Step 1: 创建通用导航布局（所有页面共享）**

```html
<!-- frontend/index.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>智能日志分析与诊断平台</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="css/style.css" rel="stylesheet">
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container-fluid">
            <a class="navbar-brand" href="index.html">🔍 日志诊断平台</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="index.html">首页</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="dashboard.html">仪表盘</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="list.html">日志列表</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="submit.html">提交日志</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- 主内容区 -->
    <main class="container mt-4">
        <div class="jumbotron">
            <h1 class="display-4">欢迎使用智能日志分析与诊断平台</h1>
            <p class="lead">快速提交异常日志，一键获取诊断分析结果</p>
            <hr class="my-4">
            <div class="d-grid gap-2 d-md-flex justify-content-md-start">
                <a class="btn btn-primary btn-lg" href="submit.html" role="button">提交日志</a>
                <a class="btn btn-outline-primary btn-lg" href="dashboard.html" role="button">查看仪表盘</a>
            </div>
        </div>
    </main>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

- [ ] **Step 2: 创建自定义样式**

```css
/* frontend/css/style.css */
/* 自定义样式覆盖和扩展 */

body {
    background-color: #f8f9fa;
}

.navbar-brand {
    font-weight: 600;
}

.jumbotron {
    background-color: #ffffff;
    border-radius: 0.5rem;
    padding: 2rem;
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

/* 表格样式 */
.table-hover tbody tr:hover {
    background-color: rgba(0, 123, 255, 0.05);
}

/* 徽章大小 */
.badge-severity {
    min-width: 70px;
}

/* 卡片阴影 */
.card {
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

/* 图表容器 */
.chart-container {
    position: relative;
    height: 300px;
    width: 100%;
}

/* Toast 通知 */
.toast-container {
    z-index: 1050;
}
```

- [ ] **Step 3: 创建 API 调用封装**

```javascript
// frontend/js/api.js
/** API 调用封装 */

const API_BASE_URL = 'http://localhost:8000/api';

/**
 * 通用 fetch 封装
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
        headers: {
            'Content-Type': 'application/json',
        },
        ...options,
    };
    
    try {
        const response = await fetch(url, config);
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: response.statusText }));
            throw new Error(error.detail || `HTTP ${response.status}`);
        }
        if (response.status === 204) {
            return null;
        }
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * 日志 API
 */
const logsApi = {
    // 创建日志
    async create(data) {
        return apiRequest('/logs', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },
    
    // 获取日志列表
    async getList(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const suffix = queryString ? `?${queryString}` : '';
        return apiRequest(`/logs${suffix}`);
    },
    
    // 获取日志详情
    async getById(id) {
        return apiRequest(`/logs/${id}`);
    },
    
    // 更新日志
    async update(id, data) {
        return apiRequest(`/logs/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },
    
    // 删除日志
    async delete(id) {
        return apiRequest(`/logs/${id}`, {
            method: 'DELETE',
        });
    },
    
    // 批量删除
    async deleteBatch(ids) {
        return apiRequest('/logs', {
            method: 'DELETE',
            body: JSON.stringify({ ids }),
        });
    },
    
    // 诊断日志
    async diagnose(id) {
        return apiRequest(`/logs/${id}/diagnose`, {
            method: 'POST',
        });
    },
    
    // 获取诊断结果
    async getDiagnosis(id) {
        return apiRequest(`/logs/${id}/diagnosis`);
    },
};

/**
 * 仪表盘 API
 */
const dashboardApi = {
    async getStats() {
        return apiRequest('/dashboard/stats');
    },
};

/**
 * 工具函数
 */
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    document.querySelector('.toast-container').appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', () => toast.remove());
}

// 格式化日期
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN');
}
```

- [ ] **Step 4: Commit**

```bash
git add frontend/index.html frontend/css/style.css frontend/js/api.js
git commit -m "feat: create frontend base layout and API utility"
```

---

## 迭代 6: 前端表单提交页面

### Task 37: 创建日志提交页面

**Files:**
- Create: `frontend/submit.html`
- Create: `frontend/js/submit.js`

- [ ] **Step 1: 创建提交页面 HTML**

```html
<!-- frontend/submit.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>提交日志 - 智能日志分析与诊断平台</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="css/style.css" rel="stylesheet">
</head>
<body>
    <!-- 导航栏（同 index.html） -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container-fluid">
            <a class="navbar-brand" href="index.html">🔍 日志诊断平台</a>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav">
                    <li class="nav-item"><a class="nav-link" href="index.html">首页</a></li>
                    <li class="nav-item"><a class="nav-link" href="dashboard.html">仪表盘</a></li>
                    <li class="nav-item"><a class="nav-link" href="list.html">日志列表</a></li>
                    <li class="nav-item"><a class="nav-link active" href="submit.html">提交日志</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <main class="container mt-4">
        <h2 class="mb-4">提交异常日志</h2>
        
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="card">
                    <div class="card-body">
                        <form id="logForm" enctype="multipart/form-data">
                            <!-- 异常类型 -->
                            <div class="mb-3">
                                <label for="exceptionType" class="form-label">异常类型 <span class="text-danger">*</span></label>
                                <select class="form-select" id="exceptionType" required>
                                    <option value="">请选择...</option>
                                    <option value="NullPointerException">NullPointerException</option>
                                    <option value="TimeoutError">TimeoutError</option>
                                    <option value="DatabaseError">DatabaseError</option>
                                    <option value="AuthenticationError">AuthenticationError</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                            
                            <!-- 严重程度 -->
                            <div class="mb-3">
                                <label class="form-label">严重程度 <span class="text-danger">*</span></label>
                                <div>
                                    <div class="form-check form-check-inline">
                                        <input class="form-check-input" type="radio" name="severity" id="severityLow" value="LOW">
                                        <label class="form-check-label" for="severityLow">Low</label>
                                    </div>
                                    <div class="form-check form-check-inline">
                                        <input class="form-check-input" type="radio" name="severity" id="severityMedium" value="MEDIUM">
                                        <label class="form-check-label" for="severityMedium">Medium</label>
                                    </div>
                                    <div class="form-check form-check-inline">
                                        <input class="form-check-input" type="radio" name="severity" id="severityHigh" value="HIGH">
                                        <label class="form-check-label" for="severityHigh">High</label>
                                    </div>
                                    <div class="form-check form-check-inline">
                                        <input class="form-check-input" type="radio" name="severity" id="severityCritical" value="CRITICAL">
                                        <label class="form-check-label" for="severityCritical">Critical</label>
                                    </div>
                                </div>
                                <div id="severityError" class="invalid-feedback d-block"></div>
                            </div>
                            
                            <!-- 日志内容 -->
                            <div class="mb-3">
                                <label for="logContent" class="form-label">日志内容 <span class="text-danger">*</span></label>
                                <textarea class="form-control" id="logContent" rows="5" placeholder="粘贴日志内容..." required></textarea>
                                <div class="form-text">或者上传日志文件（二选一）</div>
                            </div>
                            
                            <!-- 文件上传 -->
                            <div class="mb-3">
                                <label for="logFile" class="form-label">上传日志文件</label>
                                <input type="file" class="form-control" id="logFile" accept=".log,.txt">
                                <div class="form-text">支持 .log, .txt 格式</div>
                            </div>
                            
                            <!-- 发生时间 -->
                            <div class="mb-3">
                                <label for="occurredAt" class="form-label">发生时间</label>
                                <input type="datetime-local" class="form-control" id="occurredAt">
                            </div>
                            
                            <!-- 服务名称 -->
                            <div class="mb-3">
                                <label for="serviceName" class="form-label">服务名称</label>
                                <input type="text" class="form-control" id="serviceName" placeholder="例如：user-service">
                            </div>
                            
                            <!-- 堆栈跟踪 -->
                            <div class="mb-3">
                                <label for="stackTrace" class="form-label">堆栈跟踪</label>
                                <textarea class="form-control" id="stackTrace" rows="4" placeholder="可选：粘贴堆栈跟踪信息"></textarea>
                            </div>
                            
                            <!-- 用户 ID -->
                            <div class="mb-3">
                                <label for="userId" class="form-label">用户 ID / 请求 ID</label>
                                <input type="text" class="form-control" id="userId" placeholder="可选">
                            </div>
                            
                            <div class="d-grid gap-2">
                                <button type="submit" class="btn btn-primary btn-lg">提交日志</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <div class="toast-container position-fixed bottom-0 end-0 p-3"></div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="js/api.js"></script>
    <script src="js/submit.js"></script>
</body>
</html>
```

- [ ] **Step 2: 创建表单处理逻辑**

```javascript
// frontend/js/submit.js
/** 日志提交页面逻辑 */

document.getElementById('logForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // 获取表单值
    const exceptionType = document.getElementById('exceptionType').value;
    const severity = document.querySelector('input[name="severity"]:checked');
    const content = document.getElementById('logContent').value.trim();
    const file = document.getElementById('logFile').files[0];
    const occurredAt = document.getElementById('occurredAt').value;
    const serviceName = document.getElementById('serviceName').value.trim();
    const stackTrace = document.getElementById('stackTrace').value.trim();
    const userId = document.getElementById('userId').value.trim();
    
    // 验证必填项
    let isValid = true;
    
    if (!exceptionType) {
        document.getElementById('exceptionType').classList.add('is-invalid');
        isValid = false;
    } else {
        document.getElementById('exceptionType').classList.remove('is-invalid');
    }
    
    const severityError = document.getElementById('severityError');
    if (!severity) {
        severityError.textContent = '请选择严重程度';
        isValid = false;
    } else {
        severityError.textContent = '';
    }
    
    if (!content && !file) {
        document.getElementById('logContent').classList.add('is-invalid');
        document.getElementById('logFile').classList.add('is-invalid');
        showToast('日志内容或文件至少填写一项', 'warning');
        isValid = false;
    } else {
        document.getElementById('logContent').classList.remove('is-invalid');
        document.getElementById('logFile').classList.remove('is-invalid');
    }
    
    if (!isValid) {
        showToast('请修正表单错误', 'danger');
        return;
    }
    
    // 构建提交数据
    const submitData = {
        exception_type: exceptionType,
        severity: severity.value,
        service_name: serviceName || null,
        stack_trace: stackTrace || null,
        user_id: userId || null,
        occurred_at: occurredAt || null,
    };
    
    // 如果有文件，读取文件内容
    if (file) {
        try {
            const fileContent = await readFile(file);
            submitData.content = fileContent;
        } catch (err) {
            showToast('读取文件失败：' + err.message, 'danger');
            return;
        }
    } else {
        submitData.content = content;
    }
    
    // 提交 API
    try {
        const result = await logsApi.create(submitData);
        showToast('日志提交成功！', 'success');
        
        // 跳转到诊断页面
        setTimeout(() => {
            window.location.href = `diagnosis.html?id=${result.id}`;
        }, 1000);
    } catch (err) {
        showToast('提交失败：' + err.message, 'danger');
    }
});

/**
 * 读取文件内容
 */
function readFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsText(file);
    });
}

// 清除错误状态
document.getElementById('exceptionType').addEventListener('change', function() {
    this.classList.remove('is-invalid');
});

document.querySelectorAll('input[name="severity"]').forEach(radio => {
    radio.addEventListener('change', function() {
        document.getElementById('severityError').textContent = '';
    });
});
```

- [ ] **Step 3: Commit**

```bash
git add frontend/submit.html frontend/js/submit.js
git commit -m "feat: create log submission form page"
```

---

## 迭代 7: Docker 配置 + 集成测试

### Task 53: 创建 Docker 配置文件

**Files:**
- Create: `backend/Dockerfile`
- Create: `frontend/Dockerfile`
- Create: `frontend/nginx.conf`
- Create: `docker-compose.yml`

- [ ] **Step 1: 创建后端 Dockerfile**

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY backend/ ./backend/

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- [ ] **Step 2: 创建前端 Dockerfile**

```dockerfile
# frontend/Dockerfile
FROM nginx:alpine

# 复制静态文件
COPY frontend/ /usr/share/nginx/html/

# 复制 nginx 配置
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
```

- [ ] **Step 3: 创建 nginx 配置**

```nginx
# frontend/nginx.conf
server {
    listen 80;
    server_name localhost;
    
    root /usr/share/nginx/html;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # 禁止访问隐藏文件
    location ~ /\. {
        deny all;
    }
}
```

- [ ] **Step 4: 创建 docker-compose.yml**

```yaml
# docker-compose.yml
version: '3.9'

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    container_name: log-diagnosis-api
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    
  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    container_name: log-diagnosis-web
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  backend_data:
```

- [ ] **Step 5: 验证配置语法**

```bash
docker-compose config
```

- [ ] **Step 6: Commit**

```bash
git add backend/Dockerfile frontend/Dockerfile frontend/nginx.conf docker-compose.yml
git commit -m "feat: add Docker configuration for containerized deployment"
```

---

## 附录：完整任务清单

| Task | 描述 | 状态 |
|------|------|------|
| Task 1 | 项目目录结构 | ☐ |
| Task 2 | requirements.txt | ☐ |
| Task 3 | LogEntry 数据模型 | ☐ |
| Task 4 | Pydantic Schemas | ☐ |
| Task 5 | Repository 基类 | ☐ |
| Task 6 | Mock Repository | ☐ |
| Task 7 | Diagnosis 数据模型 | ☐ |
| Task 8 | Diagnosis Schemas | ☐ |
| Task 9 | 自定义异常类 | ☐ |
| Task 10 | FastAPI 主应用 | ☐ |
| Task 11 | 日志路由（创建 + 查询） | ☐ |
| Task 12 | 日志路由（详情 + 更新 + 删除） | ☐ |
| Task 21 | 诊断规则库 | ☐ |
| Task 22 | 诊断服务 | ☐ |
| Task 23 | 诊断路由 | ☐ |
| Task 30 | 仪表盘路由 | ☐ |
| Task 36 | 前端基础布局 + API 封装 | ☐ |
| Task 37 | 提交页面 | ☐ |
| Task 53 | Docker 配置 | ☐ |

---

**文档结束**
