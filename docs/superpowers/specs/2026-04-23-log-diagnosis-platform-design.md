# 智能日志分析与诊断平台 - 设计文档

**文档 ID:** SPEC-2026-04-23-001  
**创建日期:** 2026-04-23  
**状态:** 已批准  
**作者:** Claude (with user collaboration)

---

## 1. 概述

### 1.1 项目目标
开发一个"智能日志分析与诊断平台"，提供 Web 界面供用户提交异常日志、管理日志记录、并通过可视化仪表盘和一键诊断功能帮助用户快速定位和解决问题。

### 1.2 核心价值
- **降低故障排查时间**：一键诊断自动生成根因分析和建议方案
- **知识沉淀**：历史日志和诊断结果形成可检索的知识库
- **可视化洞察**：仪表盘展示异常趋势和分布，辅助决策

### 1.3 范围
- ✅ 日志提交（表单 + 文件上传）
- ✅ 日志管理（CRUD + 搜索筛选）
- ✅ 可视化仪表盘（统计图表）
- ✅ 一键诊断（规则匹配 + 大模型降级）
- ❌ 用户认证（后续迭代）
- ❌ 多租户支持（后续迭代）

---

## 2. 系统架构

### 2.1 整体架构
```
┌─────────────────────────────────────────────────────────────┐
│                      智能日志分析与诊断平台                    │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐         ┌─────────────┐                    │
│  │  Frontend   │         │  Backend    │                    │
│  │  (端口 3000) │◄───────►│  (端口 8000)│                    │
│  │  Bootstrap  │  REST   │  FastAPI    │                    │
│  │  Nginx      │  JSON   │  Uvicorn    │                    │
│  └─────────────┘         └──────┬──────┘                    │
│                                 │                            │
│                                 ▼                            │
│                        ┌─────────────┐                       │
│                        │  Repository │                       │
│                        │  (Mock 接口) │                       │
│                        └─────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 技术栈
| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | HTML5/CSS3/JavaScript ES6 | 纯原生，无构建工具 |
| UI 框架 | Bootstrap 5.3 | 响应式布局 + 组件 |
| 图表库 | Chart.js 4.x | 仪表盘统计图 |
| 后端 | Python 3.11 + FastAPI | 异步 API 服务 |
| 数据持久化 | Mock Repository | 内存存储，预留 DB 接口 |
| 部署 | Docker 24.x + Compose | 容器化部署 |

### 2.3 目录结构
```
log-diagnosis-platform/
├── frontend/
│   ├── index.html          # 首页（重定向到仪表盘）
│   ├── submit.html         # 日志提交页面
│   ├── list.html           # 日志列表页面
│   ├── dashboard.html      # 仪表盘页面
│   ├── diagnosis.html      # 诊断详情页面
│   ├── css/
│   │   └── style.css       # 自定义样式
│   └── js/
│       ├── api.js          # API 调用封装
│       ├── submit.js       # 提交页面逻辑
│       ├── list.js         # 列表页面逻辑
│       ├── dashboard.js    # 仪表盘逻辑
│       └── diagnosis.js    # 诊断页面逻辑
├── backend/
│   ├── main.py             # FastAPI 入口
│   ├── models/
│   │   ├── __init__.py
│   │   └── log_entry.py    # 日志数据模型
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── diagnosis.py    # Pydantic 请求/响应模型
│   ├── repository/
│   │   ├── __init__.py
│   │   ├── base.py         # Repository 基类（接口定义）
│   │   └── mock.py         # Mock 实现
│   ├── services/
│   │   ├── __init__.py
│   │   └── diagnosis.py    # 诊断引擎
│   └── utils/
│       └── exceptions.py   # 自定义异常
├── tests/
│   ├── unit/
│   │   ├── test_repository.py
│   │   └── test_diagnosis.py
│   └── integration/
│       └── test_api.py
├── Dockerfile              # 后端镜像
├── docker-compose.yml      # 编排配置
└── requirements.txt        # Python 依赖
```

---

## 3. 数据模型

### 3.1 LogEntry（日志条目）
```python
class LogEntry:
    id: str                    # UUID, 主键
    content: str               # 日志内容（必填）
    exception_type: str        # 异常类型（必填）
    severity: str              # LOW/MEDIUM/HIGH/CRITICAL（必填）
    occurred_at: datetime|null # 发生时间（可选）
    service_name: str|null     # 服务名称（可选）
    stack_trace: str|null      # 堆栈跟踪（可选）
    user_id: str|null          # 用户 ID（可选）
    created_at: datetime       # 创建时间（系统生成）
    updated_at: datetime       # 更新时间（系统生成）
```

### 3.2 Diagnosis（诊断结果）
```python
class Diagnosis:
    id: str                    # UUID, 主键
    log_id: str                # 关联日志 ID（外键）
    root_cause: str            # 根因分析
    solution: str              # 建议解决方案
    severity_assessment: str   # 严重程度评估
    similar_logs: list[str]    # 相似日志 ID 列表
    created_at: datetime       # 创建时间
```

### 3.3 异常类型枚举
```python
EXCEPTION_TYPES = [
    "NullPointerException",
    "TimeoutError",
    "DatabaseError",
    "AuthenticationError",
    "Other"
]
```

### 3.4 严重程度枚举
```python
SEVERITY_LEVELS = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
```

---

## 4. API 设计

### 4.1 日志管理 API

#### POST /api/logs
创建日志条目（支持文件上传）
```
Request:
  Content-Type: multipart/form-data
  body:
    - content: string (可选，与 file 二选一)
    - file: File (可选，.log/.txt)
    - exception_type: string (必填)
    - severity: string (必填)
    - occurred_at: datetime (可选)
    - service_name: string (可选)
    - stack_trace: string (可选)
    - user_id: string (可选)

Response (201 Created):
{
    "id": "uuid-string",
    "content": "...",
    "exception_type": "NullPointerException",
    "severity": "HIGH",
    "occurred_at": "2026-04-23T10:00:00Z",
    "service_name": "user-service",
    "stack_trace": "...",
    "user_id": "user-123",
    "created_at": "2026-04-23T10:05:00Z",
    "updated_at": "2026-04-23T10:05:00Z"
}
```

#### GET /api/logs
获取日志列表（分页、筛选、搜索）
```
Query Parameters:
  - page: integer (默认 1)
  - page_size: integer (默认 10, 最大 100)
  - exception_type: string (可选)
  - severity: string (可选)
  - service_name: string (可选)
  - search: string (可选，全文搜索)
  - date_from: date (可选)
  - date_to: date (可选)

Response (200 OK):
{
    "items": [...],
    "total": 150,
    "page": 1,
    "page_size": 10,
    "total_pages": 15
}
```

#### GET /api/logs/{id}
获取单条日志详情
```
Response (200 OK): LogEntry 对象
Response (404 Not Found): {"detail": "Log not found"}
```

#### PUT /api/logs/{id}
更新日志
```
Request: 同 POST (除 id 外的字段)
Response (200 OK): 更新后的 LogEntry
```

#### DELETE /api/logs/{id}
删除单条日志
```
Response (204 No Content)
```

#### DELETE /api/logs
批量删除日志
```
Request:
  Content-Type: application/json
  body: { "ids": ["uuid1", "uuid2", ...] }

Response (204 No Content)
```

### 4.2 诊断 API

#### POST /api/logs/{id}/diagnose
一键诊断
```
Response (200 OK):
{
    "id": "diag-uuid",
    "log_id": "log-uuid",
    "root_cause": "空指针异常，由于...",
    "solution": "1. 检查对象初始化...\n2. 添加 null 检查...",
    "severity_assessment": "HIGH",
    "similar_logs": ["uuid1", "uuid2"],
    "created_at": "2026-04-23T10:05:00Z"
}
```

#### GET /api/logs/{id}/diagnosis
获取已有诊断结果
```
Response (200 OK): Diagnosis 对象
Response (404 Not Found): {"detail": "Diagnosis not found"}
```

### 4.3 仪表盘 API

#### GET /api/dashboard/stats
获取仪表盘统计数据
```
Response (200 OK):
{
    "exception_type_distribution": [
        {"type": "NullPointerException", "count": 45},
        {"type": "TimeoutError", "count": 30},
        ...
    ],
    "severity_distribution": [
        {"level": "CRITICAL", "count": 10},
        {"level": "HIGH", "count": 25},
        {"level": "MEDIUM", "count": 50},
        {"level": "LOW", "count": 65}
    ],
    "trend": [
        {"date": "2026-04-16", "count": 12},
        {"date": "2026-04-17", "count": 15},
        ...
    ],
    "top_services": [
        {"service": "user-service", "count": 40},
        {"service": "order-service", "count": 35},
        ...
    ]
}
```

---

## 5. 前端页面设计

### 5.1 页面导航结构
```
┌─────────────────────────────────────────────────────────────┐
│  Logo  |  仪表盘  |  日志列表  |  提交日志  |  (导航栏)     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    页面内容区域                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 提交页面 (submit.html)
**布局:** 三栏居中表单
**字段:**
- 异常类型（下拉选择，必填）
- 严重程度（单选按钮，必填）
- 日志内容（文本域，与文件上传二选一）
- 文件上传（.log/.txt，与日志内容二选一）
- 发生时间（datetime-local，可选）
- 服务名称（文本输入，可选）
- 堆栈跟踪（文本域，可选）
- 用户 ID（文本输入，可选）
- 提交按钮

**交互:**
- 表单验证（必填项、文件类型）
- 提交成功后跳转到日志详情页

### 5.3 日志列表页面 (list.html)
**布局:** 表格 + 筛选区 + 分页器
**筛选区:**
- 异常类型（下拉多选）
- 严重程度（下拉多选）
- 服务名称（文本输入）
- 时间范围（日期选择器）
- 搜索框（关键词）
- 筛选按钮、重置按钮

**表格列:** ID、异常类型、严重程度、服务名称、发生时间、操作
**操作列:** 查看、编辑、删除、诊断

**批量操作:** 全选复选框、批量删除按钮

### 5.4 仪表盘页面 (dashboard.html)
**布局:** 2x2 网格
**图表:**
1. 异常类型分布（饼图）
2. 严重程度分布（柱状图）
3. 异常趋势（折线图，近 7 天/近 30 天切换）
4. Top 服务排名（横向柱状图）

**交互:** 时间范围选择器（近 7 天、近 30 天、自定义）

### 5.5 诊断详情页面 (diagnosis.html)
**布局:** 两栏
**左栏:** 原始日志内容（可折叠的堆栈跟踪）
**右栏:** 诊断结果
- 根因分析（卡片）
- 严重程度评估（徽章）
- 建议解决方案（步骤列表）
- 相似日志推荐（列表，可点击跳转）

---

## 6. 诊断引擎设计

### 6.1 诊断流程
```
                    ┌─────────────────┐
                    │  接收日志 ID    │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │  获取日志详情   │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
              ┌─────│  规则匹配引擎   │─────┐
              │     └─────────────────┘     │
              │  (基于异常类型 + 关键词)     │
              ▼                             ▼
    ┌─────────────────┐           ┌─────────────────┐
    │  规则匹配成功   │           │  规则匹配失败   │
    │  → 返回诊断结果 │           │  → 调用大模型   │
    └─────────────────┘           │  (Claude API)   │
                                  └────────┬────────┘
                                           ▼
                                  ┌─────────────────┐
                                  │  解析模型响应   │
                                  │  生成诊断结果   │
                                  └─────────────────┘
```

### 6.2 规则库设计
```python
DIAGNOSIS_RULES = {
    "NullPointerException": {
        "keywords": {
            "null": "对象未初始化或为 null",
            "getXXX()": "getter 方法返回 null",
            "request": "HTTP 请求对象为空"
        },
        "solution_template": [
            "检查对象初始化逻辑",
            "添加 null 检查或使用 Optional",
            " review 调用链确保上游返回有效值"
        ]
    },
    "TimeoutError": {
        "keywords": {
            "connection": "网络连接超时",
            "database": "数据库查询超时",
            "api": "外部 API 响应超时"
        },
        "solution_template": [
            "检查网络连通性",
            "增加超时阈值或添加重试机制",
            "分析慢查询并优化"
        ]
    },
    "DatabaseError": {
        "keywords": {
            "constraint": "违反数据库约束",
            "deadlock": "死锁",
            "connection": "连接池耗尽"
        },
        "solution_template": [
            "检查数据完整性和约束",
            "分析事务隔离级别",
            "调整连接池配置"
        ]
    },
    "AuthenticationError": {
        "keywords": {
            "token": "Token 过期或无效",
            "permission": "权限不足",
            "session": "会话失效"
        },
        "solution_template": [
            "刷新认证 Token",
            "检查用户权限配置",
            "重新登录"
        ]
    }
}
```

### 6.3 大模型降级策略
**触发条件:**
- 规则匹配得分 < 0.5（无明确匹配）
- 异常类型为 "Other"
- 日志内容包含复杂上下文

**Prompt 模板:**
```
你是一位资深系统诊断专家。请分析以下日志并生成诊断报告：

【日志内容】
{content}

【异常类型】
{exception_type}

【严重程度】
{severity}

【服务名称】
{service_name}

【堆栈跟踪】
{stack_trace}

请按以下格式输出诊断结果（JSON）：
{
    "root_cause": "根因分析，200 字以内",
    "solution": "建议解决方案，分步骤列出",
    "severity_assessment": "LOW/MEDIUM/HIGH/CRITICAL",
    "confidence": "匹配置信度 0-1"
}
```

### 6.4 相似日志推荐算法
**简单实现（V1）:**
- 基于异常类型 + 严重程度匹配
- 按服务名称加权
- 返回最近 5 条相似日志

**优化方向（后续迭代）:**
- TF-IDF 文本相似度
- 嵌入向量相似度（Embedding）

---

## 7. 错误处理

### 7.1 后端异常类型
```python
class LogNotFoundError(Exception):
    """日志不存在"""
    status_code = 404

class InvalidLogDataError(Exception):
    """日志数据格式错误"""
    status_code = 400

class DiagnosisNotFoundError(Exception):
    """诊断结果不存在"""
    status_code = 404

class DiagnosisAlreadyExistsError(Exception):
    """诊断结果已存在"""
    status_code = 409
```

### 7.2 统一错误响应
```json
{
    "error": {
        "code": "LOG_NOT_FOUND",
        "message": "日志 ID 'xxx' 不存在",
        "details": {}
    }
}
```

### 7.3 前端错误处理
- API 调用失败 → Toast 提示
- 表单验证失败 → 字段级红框 + 错误文字
- 404 → 跳转专用错误页
- 500 → 提示"服务器错误，请稍后重试"

---

## 8. 部署配置

### 8.1 Docker 配置
**后端 Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./backend/
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**前端 Dockerfile:**
```dockerfile
FROM nginx:alpine
COPY frontend/ /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

**docker-compose.yml:**
```yaml
version: '3.9'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - PYTHONUNBUFFERED=1

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
```

---

## 9. 测试策略

### 9.1 单元测试
- Repository 层：CRUD 操作验证
- 诊断引擎：规则匹配准确性

### 9.2 集成测试
- API 端点：使用 TestClient 模拟请求
- 完整流程：提交 → 诊断 → 查看

### 9.3 手动测试清单
- [ ] 表单提交（文本 + 文件）
- [ ] 日志列表分页
- [ ] 筛选和搜索
- [ ] 编辑和删除
- [ ] 诊断生成
- [ ] 仪表盘图表渲染

---

## 10. 后续迭代规划

### V2.0（后续）
- [ ] 用户认证（JWT）
- [ ] 角色权限管理
- [ ] 日志导出（CSV/PDF）
- [ ] 邮件告警

### V3.0（后续）
- [ ] 真实数据库支持（PostgreSQL）
- [ ] 日志自动采集（Agent）
- [ ] 实时告警看板（WebSocket）

---

## 11. 附录

### 11.1 依赖清单
```
# backend/requirements.txt
fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.5.3
python-multipart==0.0.6
pytest==7.4.4
httpx==0.26.0  # 用于测试
```

### 11.2 前端 CDN 资源
```html
<!-- Bootstrap 5.3 CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- Chart.js 4.x -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

<!-- Bootstrap Bundle JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
```

---

**文档结束**
