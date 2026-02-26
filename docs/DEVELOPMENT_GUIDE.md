# Zzy_Personal_Agent 工程开发规范

## 概述

本文档定义了 Zzy_Personal_Agent 项目的开发规范，所有新增功能、Agent 和脚本都必须遵循这些规则。

---

## 1. 项目目录结构规范

### 1.1 目录结构

```
Zzy_Personal_Agent/
├── agents/              # Agent 核心代码
│   └── xxx_agent.py
├── api/                 # API 路由
│   ├── __init__.py
│   └── routes/
│       └── __init__.py
├── core/                # 核心业务逻辑
│   ├── config.py
│   ├── database.py
│   └── llm.py
├── models/              # 数据模型
├── services/            # 服务层
├── tasks/               # 任务定义
├── tests/               # 测试代码
├── utils/               # 工具函数
├── scripts/             # 📁 工具脚本（新增脚本放这里）
│   ├── youtube/
│   ├── translation/
│   └── tools/
├── docs/                # 项目文档
├── docker/              # Docker 配置
│
├── [独立应用]/          # 独立应用（如字幕下载器）
│   ├── app/             # 应用主代码
│   ├── config/          # 配置
│   ├── static/          # 静态资源
│   ├── data/            # 数据目录
│   ├── requirements.txt
│   └── README.md
│
├── .env.example         # 环境变量示例
├── requirements.txt      # 根依赖
└── README.md
```

### 1.2 命名规范

| 类型 | 命名规则 | 示例 |
|------|----------|------|
| 目录 | 小写字母 + 下划线 | `youtube_service` |
| Python 文件 | 小写字母 + 下划线 | `youtube_agent.py` |
| Python 类 | 大驼峰命名 | `YouTubeAgent` |
| Python 函数/变量 | 小写下划线 | `get_video_info` |
| 常量 | 全大写下划线 | `MAX_RETRIES` |
| 前端文件 | 小写字母 + 连字符 | `youtube-downloader.html` |

---

## 2. 代码规范

### 2.1 Python 规范

```python
# ✅ 正确示例
import os
import sys
from typing import Optional, List, Dict
from datetime import datetime

# 相对导入（项目内模块）
from core import config
from utils import logger

# 绝对导入（外部库）
import yt_dlp
from flask import Flask

class YouTubeService:
    """YouTube 服务类"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.timeout = 30
    
    def get_video_info(self, video_id: str) -> Optional[Dict]:
        """获取视频信息"""
        pass

# 常量定义
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
```

```python
# ❌ 错误示例
import sys
sys.path.insert(0, '/absolute/path')  # 禁止硬编码绝对路径

# 缺少类型注解
def get_video_info(video_id):
    pass

# 使用 from xxx import * 
from flask import *
```

### 2.2 前端规范

```javascript
// ✅ 正确示例
const API_BASE_URL = '/api';

async function fetchVideoInfo(videoId) {
    const response = await fetch(`${API_BASE_URL}/video/${videoId}`);
    return response.json();
}

// 使用 const 而非 var
// 使用模板字符串
const url = `https://example.com/${id}`;
```

### 2.3 禁止事项

1. **禁止在代码中硬编码**
   - API 密钥
   - 绝对路径
   - 敏感配置

2. **禁止根目录散落脚本**
   - 所有 `.py` 文件必须放在对应的目录
   - 工具脚本放 `scripts/` 目录

3. **禁止重复代码**
   - 通用功能抽取到 `utils/`
   - 共享服务抽取到 `services/`

---

## 3. 模块导入规范

### 3.1 导入顺序

```python
# 1. 标准库
import os
import sys
import json
from datetime import datetime
from typing import Optional, Dict

# 2. 第三方库
import yt_dlp
from flask import Flask, jsonify
from flask_cors import CORS

# 3. 项目内部模块（相对导入）
from core import config
from services import youtube_service
from utils import logger
```

### 3.2 路径引用规范

```python
# ✅ 正确：使用相对于项目根的路径
# 文件: app/services/youtube_service.py
from core import config          # 同级目录

# ✅ 正确：使用 __file__ 构建相对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# ✅ 正确：动态添加到 sys.path
config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
sys.path.insert(0, config_dir)
from api_config import API_KEY
```

---

## 4. API 设计规范

### 4.1 RESTful 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/resource` | 获取列表 |
| GET | `/api/resource/<id>` | 获取单个 |
| POST | `/api/resource` | 创建 |
| PUT | `/api/resource/<id>` | 更新 |
| DELETE | `/api/resource/<id>` | 删除 |

### 4.2 响应格式

```python
# 成功响应
{
    "success": true,
    "data": {...},
    "message": "操作成功"
}

# 错误响应
{
    "success": false,
    "error": "错误信息",
    "code": "ERROR_CODE"
}
```

### 4.3 状态码

- `200` - 成功
- `201` - 创建成功
- `400` - 请求参数错误
- `401` - 未授权
- `404` - 资源不存在
- `500` - 服务器错误

---

## 5. 配置管理规范

### 5.1 环境变量

所有敏感配置必须使用环境变量：

```bash
# .env 文件（不提交到版本控制）
API_KEY=sk-xxx
DATABASE_URL=xxx
```

```python
# config.py
import os

API_KEY = os.environ.get('API_KEY', '')
```

### 5.2 配置文件

```
项目/
├── config/
│   ├── api_config.py      # API 配置
│   └── settings.py        # 应用设置
└── .env.example           # 环境变量示例
```

---

## 6. 文档规范

### 6.1 每个独立应用必须包含

```
my-app/
├── app/
│   └── main.py
├── config/
├── static/
├── data/
├── requirements.txt
└── README.md              # 必须包含！
```

### 6.2 README 模板

```markdown
# 应用名称

## 功能特性
- 功能1
- 功能2

## 项目结构
```
├── app/
├── config/
└── ...
```

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置
编辑 `config/xxx.py`

### 3. 运行
```bash
python app/main.py
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| /api/xxx | GET | xxx |

## 环境要求
- Python 3.8+
- xxx
```

### 6.3 代码注释

- **类**：必须包含 docstring
- **复杂函数**：必须包含 docstring 和参数说明
- **TODO/FIXME**：使用标准格式标记

```python
class YouTubeService:
    """YouTube 视频服务类
    
    Attributes:
        api_key: YouTube API 密钥
        timeout: 请求超时时间（秒）
    """
    
    def get_video_info(self, video_id: str) -> Optional[Dict]:
        """获取视频信息
        
        Args:
            video_id: YouTube 视频ID
            
        Returns:
            包含视频信息的字典，失败返回 None
            
        Raises:
            YouTubeError: API 调用失败
        """
        pass
```

---

## 7. 测试规范

### 7.1 测试文件位置

```
tests/
├── __init__.py
├── test_basic.py           # 基础测试
└── test_xxx_agent.py       # Agent 专项测试
```

### 7.2 测试用例命名

```python
def test_youtube_video_info():
    """测试获取视频信息"""
    pass

def test_download_subtitle():
    """测试字幕下载"""
    pass
```

---

## 8. 错误处理规范

### 8.1 统一错误响应

```python
class APIError(Exception):
    """API 统一错误类"""
    def __init__(self, message: str, code: str = "UNKNOWN_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)

@app.errorhandler(APIError)
def handle_api_error(error):
    return jsonify({
        "success": False,
        "error": error.message,
        "code": error.code
    }), 400
```

### 8.2 日志记录

```python
import logging

logger = logging.getLogger(__name__)

def some_function():
    try:
        # 业务逻辑
        pass
    except Exception as e:
        logger.error(f"操作失败: {e}", exc_info=True)
        raise
```

---

## 9. 部署规范

### 9.1 Docker 使用

```dockerfile
# 使用官方 Python 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "app/main.py"]
```

### 9.2 生产环境检查清单

- [ ] 所有敏感配置使用环境变量
- [ ] 日志输出到标准输出
- [ ] 错误堆栈不暴露给用户
- [ ] 使用 gunicorn/uwsgi 而非 flask 开发服务器

---

## 10. Git 提交规范

### 10.1 提交信息格式

```
<类型>: <简短描述>

<详细描述>

<关闭的Issue>
```

类型：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具

示例：
```
feat: 添加 YouTube 字幕下载功能

- 支持 txt/srt/docx/json 格式
- 集成 AI 核心观点提取
- 优化错误提示

Closes #123
```

---

## 检查清单

创建新功能时，请确认：

- [ ] 代码放在正确的目录
- [ ] 遵循命名规范
- [ ] 包含必要的 import
- [ ] 无硬编码路径/密钥
- [ ] 有 README 文档（如果是独立应用）
- [ ] 有基本的错误处理
- [ ] 有必要的注释/docstring
- [ ] 配置使用环境变量
- [ ] 代码格式规范（无 lint 警告）

---

## 附录：常用命令

```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试
python -m pytest tests/

# 代码检查
python -m flake8 .

# 启动服务
python app/main.py
```

---

*本文档由 Agent 生成，每次创建新功能时请遵循此规范*
