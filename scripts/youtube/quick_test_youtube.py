#!/usr/bin/env python3
"""
YouTube Agent 快速测试脚本
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.youtube_agent import YouTubeAgent


async def quick_test():
    """快速测试YouTube Agent"""
    print("\n" + "🎬"*30)
    print("YouTube视频智能体 - 快速测试")
    print("🎬"*30 + "\n")
    
    agent = YouTubeAgent()
    
    print("📡 测试1: 搜索视频...")
    result = await agent.run(
        query="Python编程",
        max_results=3,
        get_transcript=False,
        summary_type="concise",
        save_format="json"
    )
    
    if result.get("success"):
        print(f"✅ 搜索成功！找到 {len(result['videos'])} 个视频\n")
        
        for i, video in enumerate(result['videos'], 1):
            print(f"{i}. 📹 {video['title']}")
            print(f"   👤 频道: {video.get('channel', 'N/A')}")
            print(f"   👁️  播放量: {agent._format_number(video.get('views', 0))}")
            print(f"   ⏱️  时长: {video.get('duration', 'N/A')}")
            print(f"   🔗 链接: {video.get('url', 'N/A')}")
            print()
        
        print(f"📁 数据已保存到: {agent.output_dir}")
        print("\n✅ 测试完成！YouTube Agent 工作正常")
    else:
        print(f"❌ 测试失败: {result.get('error')}")
    
    print("\n" + "="*60)
    print("提示:")
    print("  - 要获取字幕和总结，设置 get_transcript=True")
    print("  - 要保存Markdown报告，设置 save_format='both'")
    print("  - 详细使用方法见: docs/youtube_agent_usage.md")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(quick_test())
