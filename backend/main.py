# backend/main.py
"""FastAPI 应用入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.repository.mock import MockRepository
from backend.services.diagnosis import DiagnosisService

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
from backend.routes import logs, diagnosis, dashboard

app.include_router(logs.router, prefix="/api", tags=["logs"])
app.include_router(diagnosis.router, prefix="/api", tags=["diagnosis"])
app.include_router(dashboard.router, prefix="/api", tags=["dashboard"])
