# YouTube视频智能体使用指南

## 📖 功能概述

YouTube视频智能体是一个强大的工具，可以帮你：

- 🔍 搜索YouTube视频（支持关键词、频道、时长筛选）
- 📊 分析视频数据（播放量、点赞数、评论数、订阅数）
- 📝 提取视频字幕并生成总结
- 💾 保存分析结果（JSON + Markdown格式）

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /Users/andreazhuo/AI/Zzy_Personal_Agent
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 配置环境变量

编辑 `.env` 文件：

```bash
# GLM API配置（必需）
ZHIPU_API_KEY=your_zhipu_api_key_here

# YouTube API配置（可选，用于更准确的搜索）
YOUTUBE_API_KEY=your_youtube_api_key_here
```

### 3. 运行智能体

#### 方式1：交互模式

```bash
python -m agents.youtube_agent
```

#### 方式2：代码调用

```python
import asyncio
from agents.youtube_agent import YouTubeAgent

async def main():
    agent = YouTubeAgent()
    
    result = await agent.run(
        query="Python编程教程",
        max_results=5,
        get_transcript=True,
        summary_type="concise",  # 或 "full"
        save_format="both"       # "json", "markdown", 或 "both"
    )
    
    print(f"找到 {len(result['videos'])} 个视频")
    for video in result['videos']:
        print(f"- {video['title']}")
        print(f"  播放量: {video['view_count']}")
        if video.get('summary'):
            print(f"  总结: {video['summary'][:100]}...")

asyncio.run(main())
```

## 📁 输出文件结构

```
data/youtube/
├── video_{video_id}_20240215_123456.json    # 单个视频数据
├── video_{video_id}_20240215_123456.md       # 单个视频报告
└── search_results_20240215_123456.json       # 搜索结果汇总
```

## 📊 数据格式

### JSON格式示例

```json
{
  "video_id": "abc123",
  "title": "Python入门教程",
  "url": "https://www.youtube.com/watch?v=abc123",
  "channel": "编程达人",
  "view_count": 1000000,
  "like_count": 50000,
  "comment_count": 1000,
  "duration": "15:30",
  "transcript": "完整字幕文本...",
  "summary": "视频内容总结...",
  "saved_files": [
    "data/youtube/video_abc123.json",
    "data/youtube/video_abc123.md"
  ]
}
```

### Markdown报告示例

```markdown
# YouTube视频分析报告

## 基本信息
- **视频标题**: Python入门教程
- **视频链接**: https://www.youtube.com/watch?v=abc123
- **频道**: 编程达人
- **播放量**: 100万

## 内容总结
视频讲解了Python的基础语法...

## 关键要点
1. Python安装方法
2. 基本数据类型
3. 控制流程
```

## 🎯 使用场景

### 1. 学习研究

```python
# 搜索编程教程并总结
result = await agent.run(
    query="机器学习入门",
    max_results=10,
    summary_type="concise"
)
```

### 2. 内容分析

```python
# 分析竞品视频
result = await agent.run(
    query="产品评测",
    max_results=20,
    get_transcript=True,
    summary_type="full"
)
```

### 3. 批量处理

```python
# 批量搜索多个主题
topics = ["AI", "Python", "Web开发"]
for topic in topics:
    result = await agent.run(query=topic, max_results=5)
```

## ⚙️ 高级配置

### 自定义输出目录

```python
agent = YouTubeAgent()
agent.output_dir = Path("custom/output/path")
```

### 调整总结类型

```python
# 精炼总结（3-5个要点）
summary_type="concise"

# 全文总结（详细内容）
summary_type="full"
```

### 筛选视频时长

```python
# 短视频（<4分钟）
video_duration="short"

# 中等长度（4-20分钟）
video_duration="medium"

# 长视频（>20分钟）
video_duration="long"
```

## 🔧 故障排除

### 问题1：无法获取字幕

**原因**：视频没有字幕或字幕不可用

**解决**：
- 检查视频是否有字幕
- 尝试其他视频
- 设置 `get_transcript=False` 跳过字幕获取

### 问题2：搜索结果不准确

**原因**：未配置YouTube API Key

**解决**：
1. 获取YouTube Data API Key
2. 在 `.env` 中配置 `YOUTUBE_API_KEY`
3. 重启应用

### 问题3：API调用失败

**原因**：网络问题或API限制

**解决**：
- 检查网络连接
- 确认API Key有效
- 检查API配额

## 📝 注意事项

1. **API限制**：YouTube Data API有每日调用限制
2. **字幕版权**：字幕内容受版权保护，请合理使用
3. **总结质量**：总结质量取决于视频字幕的完整性
4. **存储空间**：大量视频分析会占用磁盘空间

## 🔄 更新日志

### v1.0.0 (2024-02-15)
- ✅ 基本搜索功能
- ✅ 视频数据获取
- ✅ 字幕提取
- ✅ 内容总结
- ✅ 数据保存

## 📞 技术支持

如有问题，请：
1. 查看日志文件：`logs/app.log`
2. 运行测试：`python tests/test_youtube_agent.py`
3. 提交Issue到项目仓库

---

**Happy Coding! 🎉**
