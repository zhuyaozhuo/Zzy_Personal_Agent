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

## 📋 开发规范

所有新功能的开发必须遵循 [开发规范](./docs/DEVELOPMENT_GUIDE.md)，包括：
- 项目目录结构
- 代码命名规范
- 模块导入规范
- API 设计规范
- 文档要求
- 测试规范

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
