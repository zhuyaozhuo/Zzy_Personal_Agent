#!/usr/bin/env python3
"""
抖音视频下载工具
支持从抖音链接下载视频
"""

import os
import re
import json
import subprocess
import argparse
from pathlib import Path
from urllib.parse import urlparse, parse_qs


def parse_douyin_url(url: str) -> dict:
    """解析抖音URL，提取视频ID"""
    parsed = urlparse(url)
    
    if 'douyin.com' in url:
        if '/video/' in url:
            match = re.search(r'/video/(\d+)', url)
            if match:
                return {'type': 'video', 'video_id': match.group(1)}
        elif '/share/' in url:
            match = re.search(r'/share/([A-Za-z0-9]+)', url)
            if match:
                return {'type': 'share', 'share_id': match.group(1)}
    
    return None


def get_video_id(url: str) -> str:
    """获取视频ID"""
    parsed = parse_douyin_url(url)
    if parsed:
        if 'video_id' in parsed:
            return parsed['video_id']
        elif 'share_id' in parsed:
            return parsed['share_id']
    return None


def download_douyin_video(url: str, output_dir: str = "data/douyin") -> dict:
    """
    下载抖音视频
    
    Args:
        url: 抖音视频链接
        output_dir: 输出目录
    
    Returns:
        包含下载信息的字典
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    print(f"📥 正在下载抖音视频: {url}")
    
    video_id = get_video_id(url)
    if not video_id:
        video_id = "unknown"
    
    output_file = os.path.join(output_dir, f"douyin_{video_id}.mp4")
    
    try:
        cmd = [
            "yt-dlp",
            "-f", "best[ext=mp4]",
            "-o", output_file,
            "--no-playlist",
            "--no-warnings",
            url
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0 and os.path.exists(output_file):
            file_size = os.path.getsize(output_file) / (1024 * 1024)
            print(f"✅ 下载成功: {output_file}")
            print(f"   文件大小: {file_size:.2f} MB")
            
            return {
                "success": True,
                "video_path": output_file,
                "video_id": video_id,
                "file_size": file_size
            }
        else:
            print(f"❌ 下载失败: {result.stderr}")
            return {
                "success": False,
                "error": result.stderr
            }
            
    except subprocess.TimeoutExpired:
        print("❌ 下载超时")
        return {"success": False, "error": "Download timeout"}
    except Exception as e:
        print(f"❌ 下载出错: {e}")
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="抖音视频下载工具")
    parser.add_argument("url", help="抖音视频URL")
    parser.add_argument("--output", "-o", default="data/douyin", help="输出目录")
    
    args = parser.parse_args()
    
    result = download_douyin_video(args.url, args.output)
    
    print("\n" + "=" * 50)
    print("📋 结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
