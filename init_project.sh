#!/bin/bash

# ============================================
# Zzy_Personal_Agent 项目初始化脚本
# ============================================

set -e

PROJECT_ROOT="/Users/andreazhuo/AI/Zzy_Personal_Agent"

echo "🚀 开始初始化 Zzy_Personal_Agent 项目..."
echo "📁 项目路径: $PROJECT_ROOT"
echo ""

# 创建项目目录结构
echo "📂 创建项目目录结构..."

mkdir -p agents
mkdir -p api/routes
mkdir -p tasks
mkdir -p services
mkdir -p models
mkdir -p core
mkdir -p utils
mkdir -p docker
mkdir -p frontend/miniprogram/pages
mkdir -p frontend/web
mkdir -p tests
mkdir -p docs
mkdir -p data
mkdir -p logs

echo "✅ 目录结构创建完成"
echo ""

# 创建 __init__.py 文件
echo "📝 创建 Python 包初始化文件..."

touch agents/__init__.py
touch api/__init__.py
touch api/routes/__init__.py
touch tasks/__init__.py
touch services/__init__.py
touch models/__init__.py
touch core/__init__.py
touch utils/__init__.py
touch tests/__init__.py

echo "✅ Python 包初始化文件创建完成"
echo ""

# 创建 requirements.txt
echo "📦 创建 requirements.txt..."

cat > requirements.txt << 'EOF'
# 核心框架
langgraph>=0.2.0
langchain>=0.3.0
langchain-zhipu>=0.1.0

# Web框架
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
websockets>=12.0

# 任务调度
celery>=5.4.0
redis>=5.0.0

# 数据库
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
alembic>=1.13.0

# 数据验证
pydantic>=2.8.0
pydantic-settings>=2.4.0

# HTTP客户端
httpx>=0.27.0
aiohttp>=3.10.0

# 工具库
python-dotenv>=1.0.0
pyyaml>=6.0
requests>=2.32.0

# 日志
loguru>=0.7.0

# 测试
pytest>=8.0.0
pytest-asyncio>=0.23.0
pytest-cov>=5.0.0

# 代码质量
black>=24.0.0
flake8>=7.0.0
mypy>=1.10.0
EOF

echo "✅ requirements.txt 创建完成"
echo ""

# 创建 .env.example
echo "🔐 创建 .env.example..."

cat > .env.example << 'EOF'
# ============================================
# 环境变量配置示例
# ============================================

# LLM API配置
ZHIPU_API_KEY=your_zhipu_api_key_here
ZHIPU_MODEL=glm-4

# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/zzy_agent_db
REDIS_URL=redis://localhost:6379/0

# 应用配置
APP_NAME=Zzy_Personal_Agent
APP_ENV=development
DEBUG=true
SECRET_KEY=your_secret_key_here

# API配置
API_HOST=0.0.0.0
API_PORT=8000

# 推送服务配置
SERVERCHAN_KEY=your_serverchan_key_here
PUSHPLUS_TOKEN=your_pushplus_token_here

# 微信公众号配置
WECHAT_APP_ID=your_wechat_app_id
WECHAT_APP_SECRET=your_wechat_app_secret

# 小红书配置
XIAOHONGSHU_COOKIE=your_xiaohongshu_cookie

# 新闻API配置
NEWS_API_KEY=your_news_api_key

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
EOF

echo "✅ .env.example 创建完成"
echo ""

# 创建 .gitignore
echo "🚫 创建 .gitignore..."

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment variables
.env
.env.local
.env.*.local

# Logs
logs/
*.log

# Database
*.db
*.sqlite
*.sqlite3

# Docker
docker-compose.override.yml

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# MyPy
.mypy_cache/
.dmypy.json
dmypy.json

# Jupyter
.ipynb_checkpoints/
*.ipynb

# Data
data/
*.csv
*.json
!package.json
EOF

echo "✅ .gitignore 创建完成"
echo ""

# 创建 README.md
echo "📖 创建 README.md..."

cat > README.md << 'EOF'
# Zzy_Personal_Agent

基于 LangGraph 的个人智能体系统，提供7×24小时智能服务。

## 🎯 项目简介

这是一个基于 LangGraph 架构的个人智能体系统，专门服务于日常生活起居和学习。系统可以：

- 📰 自动推送新闻热点
- ✍️ 自动撰写公众号、小红书文章
- 🎬 自动制作和发布视频
- 📅 智能管理日程和提醒
- 💬 通过手机、电脑终端交互

## 🏗️ 系统架构

```
用户交互层 (手机APP/微信小程序/Web界面)
        ↓
    API网关层 (FastAPI + WebSocket)
        ↓
LangGraph智能体编排层 (新闻/写作/视频/日程Agent)
        ↓
    服务层 (LLM/消息队列/任务调度/数据库)
        ↓
  外部服务集成层 (公众号/小红书/视频平台/新闻API)
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/Zzy_Personal_Agent.git
cd Zzy_Personal_Agent
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的API密钥
```

### 5. 启动服务

```bash
# 启动API服务
uvicorn api.main:app --reload

# 启动Celery Worker (新终端)
celery -A tasks.celery_app worker --loglevel=info

# 启动Celery Beat (新终端)
celery -A tasks.celery_app beat --loglevel=info
```

## 📁 项目结构

```
Zzy_Personal_Agent/
├── agents/              # LangGraph智能体
├── api/                 # FastAPI服务
├── tasks/               # Celery任务
├── services/            # 外部服务集成
├── models/              # 数据模型
├── core/                # 核心配置
├── utils/               # 工具函数
├── docker/              # Docker配置
├── frontend/            # 前端代码
├── tests/               # 测试
├── docs/                # 文档
└── logs/                # 日志
```

## 🛠️ 技术栈

- **智能体框架**: LangGraph, LangChain, GLM-4
- **后端服务**: FastAPI, Celery, Redis, PostgreSQL
- **部署方案**: Docker, Nginx
- **前端交互**: 微信小程序, Web Dashboard

## 📖 详细文档

查看 [基于LangGraph的个人智能体系统架构设计.md](./基于LangGraph的个人智能体系统架构设计.md) 了解完整架构设计。

## 📝 开发计划

- [ ] 第一周：搭建基础框架和LangGraph编排
- [ ] 第二周：实现新闻Agent和推送功能
- [ ] 第三周：实现写作Agent和平台对接
- [ ] 第四周：部署上线和测试

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📧 联系方式

如有问题，请提交 Issue 或联系项目维护者。
EOF

echo "✅ README.md 创建完成"
echo ""

# 创建核心配置文件
echo "⚙️ 创建核心配置文件..."

# core/config.py
cat > core/config.py << 'EOF'
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "Zzy_Personal_Agent"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key"
    
    ZHIPU_API_KEY: str
    ZHIPU_MODEL: str = "glm-4"
    
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    SERVERCHAN_KEY: Optional[str] = None
    PUSHPLUS_TOKEN: Optional[str] = None
    
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
EOF

# core/database.py
cat > core/database.py << 'EOF'
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
EOF

# core/llm.py
cat > core/llm.py << 'EOF'
from langchain_zhipu import ChatZhipuAI
from core.config import settings


def get_llm(temperature: float = 0.7):
    return ChatZhipuAI(
        model=settings.ZHIPU_MODEL,
        temperature=temperature,
        api_key=settings.ZHIPU_API_KEY
    )


llm = get_llm()
EOF

echo "✅ 核心配置文件创建完成"
echo ""

# 创建工具文件
echo "🛠️ 创建工具文件..."

# utils/logger.py
cat > utils/logger.py << 'EOF'
import sys
from loguru import logger
from core.config import settings


def setup_logger():
    logger.remove()
    
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    
    logger.add(
        settings.LOG_FILE,
        level=settings.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="10 MB",
        retention="7 days",
        compression="zip"
    )
    
    return logger


logger = setup_logger()
EOF

# utils/helpers.py
cat > utils/helpers.py << 'EOF'
import json
from datetime import datetime
from typing import Any


def json_serializer(obj: Any) -> str:
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def load_json(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: dict, file_path: str):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=json_serializer)
EOF

echo "✅ 工具文件创建完成"
echo ""

# 创建 Docker 配置
echo "🐳 创建 Docker 配置..."

# docker/Dockerfile
cat > docker/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# docker/docker-compose.yml
cat > docker/docker-compose.yml << 'EOF'
version: '3.8'

services:
  api:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - ZHIPU_API_KEY=${ZHIPU_API_KEY}
      - REDIS_URL=redis://redis:6379/0
      - DATABASE_URL=postgresql://postgres:password@db:5432/zzy_agent
    depends_on:
      - redis
      - db
    volumes:
      - ../data:/app/data
      - ../logs:/app/logs
  
  celery_worker:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    command: celery -A tasks.celery_app worker --loglevel=info
    depends_on:
      - redis
      - db
    environment:
      - ZHIPU_API_KEY=${ZHIPU_API_KEY}
      - REDIS_URL=redis://redis:6379/0
      - DATABASE_URL=postgresql://postgres:password@db:5432/zzy_agent
    volumes:
      - ../data:/app/data
      - ../logs:/app/logs
  
  celery_beat:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    command: celery -A tasks.celery_app beat --loglevel=info
    depends_on:
      - redis
    environment:
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ../logs:/app/logs
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=zzy_agent
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  redis_data:
  postgres_data:
EOF

echo "✅ Docker 配置创建完成"
echo ""

# 创建示例测试文件
echo "🧪 创建示例测试文件..."

cat > tests/test_basic.py << 'EOF'
import pytest
from fastapi.testclient import TestClient


def test_health_check():
    """测试健康检查接口"""
    from api.main import app
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
EOF

echo "✅ 测试文件创建完成"
echo ""

# 移动架构设计文档到 docs 目录
echo "📚 整理文档..."

if [ -f "基于LangGraph的个人智能体系统架构设计.md" ]; then
    mv "基于LangGraph的个人智能体系统架构设计.md" docs/
    echo "✅ 架构设计文档已移动到 docs/ 目录"
fi

echo ""
echo "============================================"
echo "🎉 项目初始化完成！"
echo "============================================"
echo ""
echo "📋 下一步操作："
echo ""
echo "1. 配置环境变量："
echo "   cp .env.example .env"
echo "   # 编辑 .env 文件，填入你的API密钥"
echo ""
echo "2. 创建虚拟环境："
echo "   python3 -m venv venv"
echo "   source venv/bin/activate"
echo ""
echo "3. 安装依赖："
echo "   pip install -r requirements.txt"
echo ""
echo "4. 初始化Git仓库："
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Initial commit'"
echo ""
echo "5. 开始开发："
echo "   # 查看项目结构"
echo "   tree -L 2"
echo ""
echo "📖 查看详细文档："
echo "   cat docs/基于LangGraph的个人智能体系统架构设计.md"
echo ""
echo "🚀 祝你开发顺利！"
