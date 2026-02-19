# 基于LangGraph的个人智能体系统架构设计

## 📋 整体架构设计

### 1. 系统架构图

┌─────────────────────────────────────────────────────────────┐
│                    用户交互层                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │ 手机APP  │  │ 微信小程序│  │ Web界面  │                 │
│  └──────────┘  └──────────┘  └──────────┘                 │
└─────────────────────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────────────┐
│                    API网关层                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FastAPI / Flask REST API + WebSocket                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────────────┐
│              LangGraph 智能体编排层                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ 新闻Agent│  │写作Agent │  │视频Agent │  │日程Agent │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          LangGraph StateGraph 协调器                  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────────────┐
│                    服务层                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ LLM API  │  │ 消息队列  │  │ 任务调度  │  │ 数据存储  │  │
│  │(GLM/GPT) │  │ (Redis)  │  │(Celery)  │  │(PostgreSQL│  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────────────┐
│                  外部服务集成层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │公众号API │  │小红书API │  │ 视频平台 │  │ 新闻API  │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘


## 🛠️ 技术栈选择

### 核心技术栈

```yaml
智能体框架:
  - LangGraph: 智能体编排和状态管理
  - LangChain: LLM工具集成
  - GLM-4: 主要LLM模型

后端服务:
  - Python 3.11+
  - FastAPI: REST API + WebSocket
  - Celery: 异步任务调度
  - Redis: 消息队列 + 缓存
  - PostgreSQL: 持久化存储

部署方案:
  - Docker + Docker Compose
  - 云服务器 (阿里云/腾讯云/AWS)
  - Nginx: 反向代理

前端交互:
  - 微信小程序 (手机端)
  - Web Dashboard (电脑端)
  - Server酱/PushPlus: 消息推送
```

## 📁 项目结构
Zzy_Personal_Agent/
├── agents/                    # LangGraph智能体
│   ├── init .py
│   ├── news_agent.py         # 新闻热点Agent
│   ├── writing_agent.py      # 写作Agent
│   ├── video_agent.py        # 视频制作Agent
│   ├── schedule_agent.py     # 日程管理Agent
│   └── orchestrator.py       # LangGraph编排器
├── api/                       # API服务
│   ├── init .py
│   ├── main.py               # FastAPI主应用
│   ├── routes/
│   │   ├── chat.py
│   │   ├── tasks.py
│   │   └── webhooks.py
│   └── websocket.py          # WebSocket连接
├── tasks/                     # Celery任务
│   ├── init .py
│   ├── celery_app.py
│   ├── news_tasks.py
│   ├── writing_tasks.py
│   └── video_tasks.py
├── services/                  # 外部服务集成
│   ├── init .py
│   ├── wechat_mp.py          # 公众号API
│   ├── xiaohongshu.py        # 小红书API
│   ├── video_platform.py     # 视频平台API
│   └── news_api.py           # 新闻API
├── models/                    # 数据模型
│   ├── init .py
│   ├── user.py
│   ├── task.py
│   └── message.py
├── core/                      # 核心配置
│   ├── init .py
│   ├── config.py             # 配置管理
│   ├── database.py           # 数据库连接
│   └── llm.py                # LLM客户端
├── utils/                     # 工具函数
│   ├── init .py
│   ├── logger.py
│   └── helpers.py
├── docker/                    # Docker配置
│   ├── Dockerfile
│   └── docker-compose.yml
├── frontend/                  # 前端代码
│   ├── miniprogram/          # 微信小程序
│   └── web/                  # Web界面
├── tests/                     # 测试
├── docs/                      # 文档
│   ├── architecture_design.md
│   ├── 核心技术栈.yml
│   └── 系统架构图01.txt
├── requirements.txt
├── README.md
└── .env.example


## 🚀 核心代码实现

### 1. LangGraph 智能体编排器

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_zhipu import ChatZhipuAI

class AgentState(TypedDict):
    messages: Annotated[list, "对话历史"]
    current_task: str
    task_type: str
    result: str
    next_agent: str

class PersonalAgentOrchestrator:
    def __init__(self):
        self.llm = ChatZhipuAI(model="glm-4", temperature=0.7)
        self.graph = self._build_graph()
    
    def _build_graph(self):
        workflow = StateGraph(AgentState)
        
        # 添加节点
        workflow.add_node("router", self._route_task)
        workflow.add_node("news_agent", self._news_agent)
        workflow.add_node("writing_agent", self._writing_agent)
        workflow.add_node("video_agent", self._video_agent)
        workflow.add_node("schedule_agent", self._schedule_agent)
        
        # 设置入口
        workflow.set_entry_point("router")
        
        # 添加边
        workflow.add_conditional_edges(
            "router",
            self._decide_next_agent,
            {
                "news": "news_agent",
                "writing": "writing_agent",
                "video": "video_agent",
                "schedule": "schedule_agent",
                "end": END
            }
        )
        
        # 所有agent完成后结束
        for agent in ["news_agent", "writing_agent", "video_agent", "schedule_agent"]:
            workflow.add_edge(agent, END)
        
        return workflow.compile()
    
    def _route_task(self, state: AgentState):
        """路由任务到合适的Agent"""
        task = state["current_task"]
        prompt = f"""分析以下任务，判断应该由哪个智能体处理：
        
任务：{task}

可选智能体：
- news: 新闻热点相关
- writing: 写作相关（公众号、小红书等）
- video: 视频制作相关
- schedule: 日程管理相关

只返回智能体名称，不要其他内容。"""
        
        response = self.llm.invoke(prompt)
        state["task_type"] = response.content.strip().lower()
        return state
    
    def _decide_next_agent(self, state: AgentState):
        return state.get("task_type", "end")
    
    async def run(self, task: str):
        """运行智能体"""
        initial_state = {
            "messages": [],
            "current_task": task,
            "task_type": "",
            "result": "",
            "next_agent": ""
        }
        result = await self.graph.ainvoke(initial_state)
        return result
```

### 2. 新闻Agent实现

```python
from langchain_core.tools import Tool
from langchain.agents import create_openai_functions_agent
from services.news_api import NewsAPIService

class NewsAgent:
    def __init__(self):
        self.llm = ChatZhipuAI(model="glm-4")
        self.news_service = NewsAPIService()
        self.tools = self._create_tools()
    
    def _create_tools(self):
        return [
            Tool(
                name="fetch_hot_news",
                description="获取当前热点新闻",
                func=self._fetch_hot_news
            ),
            Tool(
                name="summarize_news",
                description="总结新闻要点",
                func=self._summarize_news
            ),
            Tool(
                name="push_notification",
                description="推送消息到用户",
                func=self._push_notification
            )
        ]
    
    def _fetch_hot_news(self, category: str = "科技"):
        """获取热点新闻"""
        news = self.news_service.get_hot_news(category)
        return news
    
    def _summarize_news(self, news_content: str):
        """使用LLM总结新闻"""
        prompt = f"请总结以下新闻的要点：\n\n{news_content}"
        return self.llm.invoke(prompt).content
    
    def _push_notification(self, message: str):
        """推送到用户手机"""
        # 使用Server酱或PushPlus推送
        pass
    
    async def run(self, task: str):
        """执行新闻任务"""
        # 实现新闻获取、总结、推送逻辑
        pass
```

### 3. 写作Agent实现

```python
class WritingAgent:
    def __init__(self):
        self.llm = ChatZhipuAI(model="glm-4", temperature=0.8)
        self.platforms = {
            "wechat": WeChatMPService(),
            "xiaohongshu": XiaoHongShuService()
        }
    
    async def write_article(self, topic: str, platform: str = "wechat"):
        """写文章"""
        # 1. 生成大纲
        outline = await self._generate_outline(topic)
        
        # 2. 生成正文
        article = await self._generate_content(outline, platform)
        
        # 3. 优化标题
        title = await self._generate_title(topic, article)
        
        # 4. 发布到平台
        if platform in self.platforms:
            result = await self.platforms[platform].publish(
                title=title,
                content=article
            )
            return result
        
        return {"title": title, "content": article}
    
    async def _generate_outline(self, topic: str):
        prompt = f"为主题'{topic}'生成一个详细的文章大纲"
        return self.llm.invoke(prompt).content
    
    async def _generate_content(self, outline: str, platform: str):
        style_guide = {
            "wechat": "公众号风格：正式、专业、有深度",
            "xiaohongshu": "小红书风格：轻松、活泼、emoji丰富"
        }
        
        prompt = f"""根据以下大纲写一篇文章：
        
大纲：
{outline}

风格要求：{style_guide.get(platform, '通用风格')}"""
        
        return self.llm.invoke(prompt).content
```

### 4. Celery任务调度

```python
from celery import Celery
from celery.schedules import crontab

app = Celery('personal_agent', broker='redis://localhost:6379/0')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # 每天早上8点推送新闻
    sender.add_periodic_task(
        crontab(hour=8, minute=0),
        morning_news_push.s(),
        name='morning-news-push'
    )
    
    # 每小时检查日程
    sender.add_periodic_task(
        crontab(minute=0),
        check_schedule.s(),
        name='hourly-schedule-check'
    )

@app.task
def morning_news_push():
    """早晨新闻推送"""
    from agents.news_agent import NewsAgent
    agent = NewsAgent()
    # 获取热点新闻并推送
    news = agent.fetch_hot_news()
    summary = agent.summarize_news(news)
    agent.push_notification(summary)

@app.task
def check_schedule():
    """检查日程提醒"""
    from agents.schedule_agent import ScheduleAgent
    agent = ScheduleAgent()
    agent.check_and_remind()
```

### 5. FastAPI主应用

```python
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from agents.orchestrator import PersonalAgentOrchestrator

app = FastAPI(title="Personal Agent System")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = PersonalAgentOrchestrator()

@app.post("/api/chat")
async def chat(message: str):
    """对话接口"""
    result = await orchestrator.run(message)
    return {"result": result}

@app.post("/api/task/create")
async def create_task(task: dict):
    """创建任务"""
    # 提交到Celery队列
    from tasks.celery_app import process_task
    task_id = process_task.delay(task).id
    return {"task_id": task_id}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket连接，实时通信"""
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        result = await orchestrator.run(data)
        await websocket.send_json(result)
```

### 6. Docker部署配置

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ZHIPU_API_KEY=${ZHIPU_API_KEY}
      - REDIS_URL=redis://redis:6379/0
      - DATABASE_URL=postgresql://user:pass@db:5432/agent_db
    depends_on:
      - redis
      - db
    volumes:
      - ./data:/app/data
  
  celery_worker:
    build: .
    command: celery -A tasks.celery_app worker --loglevel=info
    depends_on:
      - redis
    environment:
      - ZHIPU_API_KEY=${ZHIPU_API_KEY}
  
  celery_beat:
    build: .
    command: celery -A tasks.celery_app beat --loglevel=info
    depends_on:
      - redis
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=agent_db
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api

volumes:
  postgres_data:
```

## 📱 手机交互方案

### 方案1：微信小程序

```javascript
// miniprogram/pages/index/index.js
Page({
  data: {
    messages: []
  },
  
  onLoad() {
    this.connectWebSocket()
  },
  
  connectWebSocket() {
    wx.connectSocket({
      url: 'wss://your-domain.com/ws/' + wx.getStorageSync('userId')
    })
    
    wx.onSocketMessage(res => {
      const data = JSON.parse(res.data)
      this.setData({
        messages: [...this.data.messages, data]
      })
    })
  },
  
  sendMessage(e) {
    const message = e.detail.value
    wx.sendSocketMessage({
      data: JSON.stringify({ message })
    })
  }
})
```

### 方案2：消息推送

```python
import requests

class PushService:
    """Server酱推送服务"""
    
    def __init__(self, send_key: str):
        self.send_key = send_key
        self.api_url = f"https://sctapi.ftqq.com/{send_key}.send"
    
    def push(self, title: str, content: str):
        """推送消息到微信"""
        data = {
            "title": title,
            "desp": content
        }
        response = requests.post(self.api_url, data=data)
        return response.json()
```

## 🚀 部署步骤

### 1. 云服务器准备

```bash
# 购买云服务器（推荐配置）
# - CPU: 2核
# - 内存: 4GB
# - 存储: 50GB SSD
# - 带宽: 3Mbps
# - 系统: Ubuntu 22.04

# 连接服务器
ssh root@your-server-ip

# 安装Docker
curl -fsSL https://get.docker.com | bash
systemctl start docker
systemctl enable docker

# 安装Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### 2. 部署应用

```bash
# 克隆项目
git clone https://github.com/yourusername/Zzy_Personal_Agent.git
cd Zzy_Personal_Agent

# 配置环境变量
cp .env.example .env
nano .env  # 填写API密钥等配置

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 检查服务状态
docker-compose ps
```

### 3. 配置域名和SSL

```bash
# 安装Nginx
apt install nginx

# 配置域名
nano /etc/nginx/sites-available/your-domain.com

# 申请SSL证书
apt install certbot python3-certbot-nginx
certbot --nginx -d your-domain.com
```

## 💰 成本估算

云服务器（阿里云/腾讯云）:

- 2核4G配置: ¥100-200/月
- 带宽3Mbps: ¥50/月
LLM API调用:

- GLM-4: ¥0.1/千tokens
- 预估月调用: ¥100-300
其他服务:

- 域名: ¥50/年
- SSL证书: 免费
总计: ¥250-550/月


## 📊 监控和维护

```python
# 添加健康检查
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "redis": check_redis(),
            "database": check_db(),
            "celery": check_celery()
        }
    }

# 日志记录
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)
```

## 🎯 下一步行动

### 1. 立即开始

```bash
# 创建项目目录
cd /Users/andreazhuo/AI/20260215/Zzy_Personal_Agent

# 初始化Git
git init

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install langgraph langchain fastapi celery redis
```

### 2. 分阶段实现

- 第一周：搭建基础框架和LangGraph编排
- 第二周：实现新闻Agent和推送功能
- 第三周：实现写作Agent和平台对接
- 第四周：部署上线和测试

### 3. 获取API密钥

- GLM API: https://open.bigmodel.cn
- Server酱: https://sct.ftqq.com
- 新闻API: https://newsapi.org

## 📝 功能清单

### 核心功能
- [ ] 新闻热点推送
- [ ] 公众号文章写作
- [ ] 小红书内容创作
- [ ] 视频制作与发布
- [ ] 日程管理与提醒

### 扩展功能
- [ ] 学习笔记整理
- [ ] 知识库管理
- [ ] 智能问答助手
- [ ] 数据分析与报告
- [ ] 自动化工作流

## 🔐 安全建议

1. **API密钥管理**
   - 使用环境变量存储敏感信息
   - 定期轮换API密钥
   - 限制API调用频率

2. **数据安全**
   - 数据库定期备份
   - 敏感数据加密存储
   - 访问日志审计

3. **网络安全**
   - 使用HTTPS加密通信
   - 设置防火墙规则
   - 定期更新系统补丁

## 📞 技术支持

如需进一步帮助，可以参考以下资源：
- LangGraph文档: https://langchain-ai.github.io/langgraph/
- FastAPI文档: https://fastapi.tiangolo.com/
- Celery文档: https://docs.celeryq.dev/
- GLM API文档: https://open.bigmodel.cn/dev/api