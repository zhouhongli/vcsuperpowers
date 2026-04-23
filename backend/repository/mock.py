# backend/repository/mock.py
"""Mock Repository 实现 - 内存存储"""
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from .base import RepositoryBase
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
