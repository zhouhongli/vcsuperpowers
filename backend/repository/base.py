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
