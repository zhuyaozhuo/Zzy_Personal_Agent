#!/usr/bin/env python3
"""
搜索查理芒格演讲视频并提取字幕
"""

import asyncio
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from agents.youtube_agent import YouTubeAgent
from utils.logger import logger


async def search_munger_speeches():
    """搜索查理芒格演讲视频"""
    
    print("\n" + "="*70)
    print("🎬 查理芒格演讲视频搜索与字幕提取")
    print("="*70 + "\n")
    
    agent = YouTubeAgent()
    
    print("📡 正在搜索查理芒格演讲视频...")
    
    search_result = agent._search_youtube("Charlie Munger speech", max_results=15)
    
    if not search_result.get("success"):
        print(f"❌ 搜索失败: {search_result.get('error')}")
        return
    
    videos = search_result.get("videos", [])
    
    print(f"找到 {len(videos)} 个视频，正在获取详细信息...\n")
    
    videos_with_data = []
    for video in videos:
        details_result = agent._get_video_details(video["video_id"])
        if details_result.get("success"):
            video_data = {**video, **details_result.get("details", {})}
            views = video_data.get("view_count", video_data.get("views", 0))
            if isinstance(views, str):
                views = agent._parse_views(views)
            videos_with_data.append((views, video_data))
    
    videos_with_data.sort(key=lambda x: x[0], reverse=True)
    
    top_videos = videos_with_data[:3]
    
    print("="*70)
    print("📊 播放量最高的3个查理芒格演讲视频")
    print("="*70 + "\n")
    
    results = []
    
    for i, (views, video) in enumerate(top_videos, 1):
        print(f"\n{'='*70}")
        print(f"📹 视频 {i}: {video['title']}")
        print(f"{'='*70}")
        print(f"   👤 频道: {video.get('channel', 'N/A')}")
        print(f"   👁️  播放量: {agent._format_number(views)}")
        print(f"   👍 点赞数: {agent._format_number(video.get('like_count', 0))}")
        print(f"   💬 评论数: {agent._format_number(video.get('comment_count', 0))}")
        print(f"   ⏱️  时长: {video.get('duration', 'N/A')} 秒")
        print(f"   🔗 链接: {video.get('url', 'N/A')}")
        
        print(f"\n   📝 正在提取字幕...")
        transcript_result = agent._get_video_transcript(video["video_id"])
        
        if transcript_result.get("success"):
            transcript = transcript_result.get("full_text", "")
            transcript_length = len(transcript)
            print(f"   ✅ 字幕提取成功！长度: {transcript_length} 字符")
            print(f"\n   📄 字幕预览 (前500字符):")
            print(f"   {'-'*66}")
            print(f"   {transcript[:500]}...")
            print(f"   {'-'*66}")
            
            video["transcript"] = transcript
            video["transcript_length"] = transcript_length
        else:
            error = transcript_result.get("error", "未知错误")
            print(f"   ⚠️  字幕提取失败: {error}")
            video["transcript"] = None
        
        video["view_count"] = views
        results.append(video)
        
        save_result = agent._save_video_data(video, f"munger_speech_{i}", format="both")
        if save_result.get("success"):
            print(f"\n   💾 数据已保存:")
            for f in save_result.get("saved_files", []):
                print(f"      📄 {f}")
        
        print()
    
    print("\n" + "="*70)
    print("✅ 任务完成！")
    print("="*70)
    
    print(f"\n📁 数据保存位置: {agent.output_dir}")
    print("\n生成的文件:")
    for i in range(1, 4):
        json_file = agent.output_dir / f"munger_speech_{i}.json"
        md_file = agent.output_dir / f"munger_speech_{i}.md"
        if json_file.exists():
            print(f"   📄 {json_file.name}")
        if md_file.exists():
            print(f"   📄 {md_file.name}")
    
    return results


if __name__ == "__main__":
    asyncio.run(search_munger_speeches())
