"""
YouTube Agent 测试文件
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.youtube_agent import YouTubeAgent
from utils.logger import logger


async def test_basic_search():
    """测试基本搜索功能"""
    print("\n" + "="*60)
    print("测试1: 基本搜索功能")
    print("="*60)
    
    agent = YouTubeAgent()
    
    result = await agent.run(
        query="Python编程教程",
        max_results=3,
        get_transcript=False,
        summary_type="concise",
        save_format="json"
    )
    
    if result.get("success"):
        print(f"✅ 搜索成功！找到 {len(result['videos'])} 个视频")
        for i, video in enumerate(result['videos'], 1):
            print(f"\n{i}. {video['title']}")
            print(f"   频道: {video.get('channel', 'N/A')}")
            print(f"   播放量: {video.get('views', 0)}")
    else:
        print(f"❌ 搜索失败: {result.get('error')}")


async def test_with_transcript():
    """测试带字幕获取的功能"""
    print("\n" + "="*60)
    print("测试2: 带字幕获取和总结")
    print("="*60)
    
    agent = YouTubeAgent()
    
    result = await agent.run(
        query="AI人工智能",
        max_results=2,
        get_transcript=True,
        summary_type="concise",
        save_format="both"
    )
    
    if result.get("success"):
        print(f"✅ 分析成功！")
        for video in result['videos']:
            print(f"\n视频: {video['title']}")
            if video.get('summary'):
                print(f"总结: {video['summary'][:200]}...")
    else:
        print(f"❌ 分析失败: {result.get('error')}")


async def test_save_functionality():
    """测试保存功能"""
    print("\n" + "="*60)
    print("测试3: 数据保存功能")
    print("="*60)
    
    agent = YouTubeAgent()
    
    test_data = {
        "video_id": "test123",
        "title": "测试视频",
        "channel": "测试频道",
        "views": 1000000,
        "summary": "这是一个测试总结"
    }
    
    result = agent._save_video_data(
        test_data,
        "test_video",
        format="both"
    )
    
    if result.get("success"):
        print(f"✅ 保存成功！")
        print(f"文件路径: {result['saved_files']}")
    else:
        print(f"❌ 保存失败: {result.get('error')}")


def test_interactive_mode():
    """测试交互模式"""
    print("\n" + "="*60)
    print("测试4: 交互模式")
    print("="*60)
    
    agent = YouTubeAgent()
    agent.interactive_search()


async def run_all_tests():
    """运行所有测试"""
    print("\n" + "🚀"*30)
    print("YouTube Agent 测试套件")
    print("🚀"*30)
    
    await test_basic_search()
    await test_save_functionality()
    
    print("\n" + "="*60)
    print("所有基础测试完成！")
    print("="*60)
    
    print("\n提示:")
    print("1. 要测试字幕获取功能，请先安装: pip install youtube-transcript-api")
    print("2. 要测试完整功能，请运行: python -m agents.youtube_agent")
    print("3. 数据文件保存在: data/youtube/")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
