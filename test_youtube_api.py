#!/usr/bin/env python3
"""
YouTube API 配置测试脚本
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def test_api_key():
    """测试YouTube API密钥配置"""
    print("\n" + "="*60)
    print("YouTube API 配置测试")
    print("="*60 + "\n")
    
    api_key = os.getenv('YOUTUBE_API_KEY')
    
    if not api_key or api_key == 'your_youtube_api_key_here':
        print("❌ 未配置YouTube API密钥")
        print("\n请按照以下步骤配置：")
        print("1. 访问 https://console.cloud.google.com/")
        print("2. 创建项目并启用YouTube Data API v3")
        print("3. 创建API密钥")
        print("4. 将密钥添加到 .env 文件：")
        print("   YOUTUBE_API_KEY=你的API密钥")
        print("\n详细步骤请查看: docs/youtube_api_setup.md")
        return False
    
    print(f"✅ API密钥已配置: {api_key[:10]}...{api_key[-10:]}")
    
    try:
        from googleapiclient.discovery import build
        
        print("\n📡 测试API连接...")
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        request = youtube.search().list(
            part='snippet',
            q='Python',
            maxResults=3,
            type='video'
        )
        response = request.execute()
        
        print(f"✅ API连接成功！找到 {len(response['items'])} 个视频\n")
        
        for i, item in enumerate(response['items'], 1):
            title = item['snippet']['title']
            channel = item['snippet']['channelTitle']
            print(f"{i}. {title}")
            print(f"   频道: {channel}\n")
        
        print("="*60)
        print("✅ YouTube API 配置成功！")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n❌ API连接失败: {e}")
        print("\n可能的原因：")
        print("1. API密钥无效")
        print("2. YouTube Data API v3 未启用")
        print("3. API密钥权限限制")
        print("4. 网络连接问题")
        print("\n请检查配置并重试")
        return False


def test_without_api():
    """测试无API密钥时的备用方案"""
    print("\n" + "="*60)
    print("测试备用搜索方案（无需API密钥）")
    print("="*60 + "\n")
    
    try:
        from youtube_search import YoutubeSearch
        
        print("📡 使用 youtube-search 库搜索...")
        results = YoutubeSearch('Python编程', max_results=3).to_dict()
        
        print(f"✅ 搜索成功！找到 {len(results)} 个视频\n")
        
        for i, video in enumerate(results, 1):
            print(f"{i}. {video['title']}")
            print(f"   频道: {video['channel']}")
            print(f"   播放量: {video['views']}\n")
        
        print("="*60)
        print("✅ 备用方案可用！")
        print("="*60)
        return True
        
    except ImportError:
        print("❌ youtube-search 库未安装")
        print("运行: pip install youtube-search")
        return False
    except Exception as e:
        print(f"❌ 搜索失败: {e}")
        return False


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('YOUTUBE_API_KEY')
    
    if api_key and api_key != 'your_youtube_api_key_here':
        test_api_key()
    else:
        print("\n💡 提示：未配置YouTube API密钥，使用备用方案")
        test_without_api()
        print("\n" + "="*60)
        print("要使用完整的YouTube API功能，请配置API密钥")
        print("详细步骤请查看: docs/youtube_api_setup.md")
        print("="*60)
