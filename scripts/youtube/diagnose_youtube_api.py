#!/usr/bin/env python3
"""
YouTube API 诊断脚本
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()


def test_network():
    """测试网络连接"""
    print("\n📡 测试网络连接...")
    
    import socket
    
    hosts = [
        ("google.com", 443),
        ("youtube.com", 443),
        ("googleapis.com", 443),
    ]
    
    for host, port in hosts:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                print(f"  ✅ {host}:{port} - 可访问")
            else:
                print(f"  ❌ {host}:{port} - 不可访问")
        except Exception as e:
            print(f"  ❌ {host}:{port} - 错误: {e}")


def test_api_key():
    """测试API密钥"""
    print("\n🔑 测试API密钥...")
    
    api_key = os.getenv('YOUTUBE_API_KEY')
    
    if not api_key:
        print("  ❌ 未配置API密钥")
        return False
    
    print(f"  ✅ API密钥已配置: {api_key[:10]}...{api_key[-10:]}")
    
    import requests
    
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q=test&maxResults=1&key={api_key}"
    
    try:
        print("\n  发送测试请求...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("  ✅ API密钥有效！")
            data = response.json()
            print(f"  ✅ 返回数据: {len(data.get('items', []))} 条结果")
            return True
        elif response.status_code == 400:
            print("  ❌ API密钥无效")
            print(f"  错误: {response.text[:200]}")
        elif response.status_code == 403:
            print("  ❌ API访问被拒绝")
            print(f"  可能原因: YouTube Data API v3 未启用")
            print(f"  错误: {response.text[:200]}")
        else:
            print(f"  ❌ 请求失败: HTTP {response.status_code}")
            print(f"  错误: {response.text[:200]}")
    except requests.exceptions.Timeout:
        print("  ❌ 请求超时 - 网络无法访问Google服务")
        print("  💡 建议: 检查网络连接或使用VPN")
    except requests.exceptions.ConnectionError as e:
        print(f"  ❌ 连接错误: {e}")
        print("  💡 建议: 检查网络连接或使用VPN")
    except Exception as e:
        print(f"  ❌ 未知错误: {e}")
    
    return False


def test_youtube_search():
    """测试备用搜索方案"""
    print("\n🔄 测试备用搜索方案 (youtube-search)...")
    
    try:
        from youtube_search import YoutubeSearch
        
        results = YoutubeSearch('Python', max_results=2).to_dict()
        print(f"  ✅ 备用方案可用！找到 {len(results)} 个视频")
        
        for i, video in enumerate(results, 1):
            print(f"     {i}. {video['title'][:50]}...")
        
        return True
    except ImportError:
        print("  ❌ youtube-search 未安装")
        print("  💡 运行: pip install youtube-search")
    except Exception as e:
        print(f"  ❌ 搜索失败: {e}")
    
    return False


def main():
    print("\n" + "="*60)
    print("YouTube API 诊断工具")
    print("="*60)
    
    test_network()
    
    api_ok = test_api_key()
    
    if not api_ok:
        test_youtube_search()
    
    print("\n" + "="*60)
    print("诊断完成")
    print("="*60)
    
    print("\n📋 建议:")
    print("  1. 如果网络无法访问Google，请使用VPN")
    print("  2. 确保在Google Cloud Console中启用了YouTube Data API v3")
    print("  3. 备用方案 (youtube-search) 无需API密钥即可使用")


if __name__ == "__main__":
    main()
