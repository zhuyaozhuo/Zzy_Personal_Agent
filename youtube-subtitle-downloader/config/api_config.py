# API配置文件
# 重要：所有敏感 API Key 请通过环境变量设置，不要硬编码在代码中！
# 复制 .env.example 为 .env 并填入你的 API Key

import os
from pathlib import Path

# 尝试从 .env 文件加载环境变量（如果存在）
env_file = Path(__file__).parent.parent.parent / ".env"
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)

# 硅基流动API Key (从环境变量读取)
# 申请地址: https://cloud.siliconflow.cn/account/ak
# 注册送¥14免费额度
SILICONFLOW_API_KEY = os.environ.get('SILICONFLOW_API_KEY', '')

# OpenAI API Key (从环境变量读取)
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')

# B站 Cookie (从环境变量读取)
# 登录B站后，在开发者工具中获取 SESSDATA 值
# 获取方法：登录B站 -> F12 -> Application -> Cookies -> bilibili.com -> SESSDATA
# 填入后即可获取AI字幕
BILIBILI_SESSDATA = os.environ.get('BILIBILI_SESSDATA', '')
