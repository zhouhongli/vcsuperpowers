# backend/routes/dashboard.py
"""仪表盘路由"""
from fastapi import APIRouter

from backend.main import repository

router = APIRouter()


@router.get("/dashboard/stats")
def get_dashboard_stats():
    """获取仪表盘统计数据"""
    return repository.get_stats()
