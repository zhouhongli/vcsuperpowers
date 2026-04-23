# 智能日志分析与诊断平台

一个基于 FastAPI 和 Bootstrap 的 Web 应用，用于提交、管理和诊断异常日志。

## 功能特性

- ✅ 日志提交（表单输入）
- ✅ 日志管理（CRUD 操作）
- ✅ 可视化仪表盘（统计图表）
- ✅ 一键诊断（规则匹配引擎）
- ✅ Docker 支持

## 技术栈

**后端:**
- Python 3.11 + FastAPI
- Pydantic (数据验证)
- Mock Repository (内存存储，预留 DB 接口)

**前端:**
- HTML5/CSS3/JavaScript ES6
- Bootstrap 5.3
- Chart.js 4.x (仪表盘)

## 快速开始

### 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 启动后端 (端口 8000)
cd backend
uvicorn main:app --reload --port 8000

# 前端（使用任意静态文件服务器或直接在浏览器打开 frontend/index.html）
```

### Docker 运行

```bash
docker-compose up --build
```

访问：
- 前端：http://localhost:3000
- 后端 API: http://localhost:8000
- API 文档：http://localhost:8000/docs

## API 端点

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/logs | 创建日志 |
| GET | /api/logs | 获取日志列表 |
| GET | /api/logs/{id} | 获取日志详情 |
| PUT | /api/logs/{id} | 更新日志 |
| DELETE | /api/logs/{id} | 删除日志 |
| DELETE | /api/logs | 批量删除 |
| POST | /api/logs/{id}/diagnose | 诊断日志 |
| GET | /api/dashboard/stats | 仪表盘统计 |

## 项目结构

```
log-diagnosis-platform/
├── backend/
│   ├── main.py              # FastAPI 入口
│   ├── models/              # 数据模型
│   ├── schemas/             # Pydantic 模型
│   ├── repository/          # 数据访问层
│   ├── services/            # 业务逻辑
│   ├── routes/              # API 路由
│   └── utils/               # 工具函数
├── frontend/
│   ├── index.html           # 首页
│   ├── submit.html          # 提交页面
│   ├── list.html            # 列表页面 (待实现)
│   ├── dashboard.html       # 仪表盘页面 (待实现)
│   ├── diagnosis.html       # 诊断详情页 (待实现)
│   ├── css/
│   └── js/
├── tests/
├── requirements.txt
└── docker-compose.yml
```

## 待实现功能

以下页面已在前端的计划中，但尚未完成：
- 日志列表页面 (list.html)
- 仪表盘页面 (dashboard.html)
- 诊断详情页面 (diagnosis.html)

## 开发说明

- 所有测试：`pytest`
- 单元测试：`pytest tests/unit/`
- 集成测试：`pytest tests/integration/`

## 许可证

MIT
