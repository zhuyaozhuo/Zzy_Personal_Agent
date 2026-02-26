# YouTube 字幕下载器 - 使用说明

一个美观易用的 YouTube 字幕下载工具，支持多种格式和翻译功能。

## 功能特点

- 支持多种格式下载（TXT、SRT、DOCX、JSON）
- 智能断句处理
- 多语言翻译支持
- 下载历史记录
- 响应式设计，支持手机端
- 视频信息预览

## 安装依赖

```bash
pip install flask flask-cors yt-dlp python-docx googletrans requests
```

## 启动服务

1. 启动后端 API 服务：

```bash
python youtube_subtitle_api.py
```

服务将在 `http://localhost:5000` 启动。

2. 在浏览器中打开前端页面：

```bash
open youtube-subtitle-downloader.html
```

或直接双击 `youtube-subtitle-downloader.html` 文件。

## 使用方法

### 1. 获取视频信息

- 在输入框中粘贴 YouTube 视频链接
- 点击"获取视频信息"按钮
- 等待视频信息加载完成

### 2. 选择选项

- **字幕语言**：选择原始字幕或指定语言
- **输出格式**：选择下载格式（TXT/SRT/DOCX/JSON）
- **翻译选项**：选择是否翻译及目标语言
- **断句处理**：选择智能断句、原始格式或合并短句

### 3. 下载字幕

- 点击对应的下载按钮
- 字幕文件将自动下载到你的电脑

## API 接口说明

### 获取视频信息

```
GET /api/video/<video_id>
```

返回视频的详细信息，包括标题、缩略图、观看次数、点赞数等。

### 下载字幕

```
POST /api/download
Content-Type: application/json

{
  "video_id": "T5-re2X-YSY",
  "format": "txt",
  "language": "zh-CN",
  "translate": "zh-CN",
  "sentence": "auto"
}
```

参数说明：
- `video_id`: YouTube 视频 ID（必填）
- `format`: 输出格式，可选值：txt、srt、docx、json
- `language`: 字幕语言代码
- `translate`: 翻译目标语言代码，"none" 表示不翻译
- `sentence`: 断句模式，"auto" 智能断句、"original" 原始格式、"merge" 合并短句

## 文件说明

- `youtube-subtitle-downloader.html` - 前端页面
- `youtube_subtitle_api.py` - 后端 API 服务
- `data/youtube/` - 数据存储目录

## 注意事项

1. 确保网络连接正常，能够访问 YouTube
2. 某些视频可能没有字幕或自动生成字幕
3. 翻译功能依赖 Google Translate，可能需要网络代理
4. 大量请求可能会被 YouTube 限制

## 故障排除

### 无法获取视频信息

- 检查视频链接是否正确
- 确认网络连接正常
- 尝试更新 yt-dlp 到最新版本

### 字幕下载失败

- 确认视频有可用字幕
- 检查语言代码是否正确
- 查看后端控制台错误信息

### 翻译不工作

- 检查网络代理设置
- 确认 googletrans 库已正确安装
- 尝试更换目标语言

## 技术栈

- 前端：HTML + CSS + JavaScript
- 后端：Python + Flask
- 字幕提取：yt-dlp
- 文档生成：python-docx
- 翻译：googletrans

## 许可证

MIT License
