# 视频字幕下载器

一个功能强大的 YouTube/B站 视频字幕下载工具，支持多种格式输出（txt、srt、docx、json），并集成 AI 核心观点提取功能。

## 功能特性

- 🎬 支持 YouTube 和 B站 两大平台
- 📝 支持多种字幕格式下载：
  - **TXT** - 纯文本格式，包含视频信息和 AI 提取的核心观点
  - **SRT** - 标准字幕格式
  - **DOCX** - Word 文档格式，排版精美
  - **JSON** - JSON 数据格式
- 🤖 支持 AI 核心观点自动提取（基于硅基流动 API）
- 🌐 支持多语言字幕和翻译
- 📱 响应式 Web 界面

## 项目结构

```
youtube-subtitle-downloader/
├── app/
│   ├── __init__.py
│   └── youtube_subtitle_api.py    # Flask API 主程序
├── config/
│   └── api_config.py              # API 配置文件
├── static/
│   └── youtube-subtitle-downloader.html  # 前端页面
├── data/
│   └── youtube/                   # 下载的字幕数据
├── requirements.txt               # Python 依赖
└── README.md                      # 本文档
```

## 快速开始

### 1. 安装依赖

```bash
cd youtube-subtitle-downloader
pip install -r requirements.txt
```

### 2. 配置 API（可选）

编辑 `config/api_config.py`，添加你的 API 密钥：

```python
# 硅基流动 API Key（用于 AI 核心观点提取）
SILICONFLOW_API_KEY = "your-api-key-here"
```

> 💡 不配置 API 也能使用基础功能，但不会生成 AI 核心观点。

### 3. 启动服务

```bash
cd app
python youtube_subtitle_api.py
```

服务启动后，访问 http://localhost:5002

## 使用方法

1. 在输入框中粘贴 YouTube 视频链接或视频 ID
2. 点击"获取视频信息"
3. 选择字幕语言、翻译语言和句子模式
4. 选择下载格式，点击下载按钮

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | Web 界面 |
| `/api/video/<video_id>` | GET | 获取视频信息 |
| `/api/download` | POST | 下载字幕 |
| `/api/health` | GET | 健康检查 |

### 下载接口示例

```bash
curl -X POST http://localhost:5002/api/download \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "xxxxx",
    "format": "txt",
    "language": "en",
    "translate": "zh-CN",
    "sentence": "auto"
  }'
```

参数说明：
- `video_id` - YouTube 视频 ID
- `format` - 输出格式：`txt`, `srt`, `docx`, `json`
- `language` - 字幕语言代码（如 `en`, `zh-CN`）
- `translate` - 翻译目标语言（如 `zh-CN`，设为 `none` 则不翻译）
- `sentence` - 句子模式：`auto` 或 `none`

## 环境要求

- Python 3.8+
- FFmpeg（推荐安装，用于更好的视频处理）

## 依赖库

- Flask - Web 框架
- Flask-CORS - 跨域支持
- yt-dlp - YouTube 视频下载
- python-docx - Word 文档生成
- requests - HTTP 请求

## 注意事项

1. 部分视频可能没有字幕，可尝试选择其他语言
2. AI 核心观点提取需要配置 API Key
3. 字幕获取依赖于 YouTube 的可访问性

## 许可证

MIT License
