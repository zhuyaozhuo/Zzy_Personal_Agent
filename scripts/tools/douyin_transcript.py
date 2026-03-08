#!/usr/bin/env python3
"""
抖音视频语音转文字工具
整合视频下载、音频转录、文本优化功能
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.douyin_downloader import download_douyin_video
from tools.video_to_text import video_to_text as vt
from tools.text_refine import refine_text


WORKSPACE_DIR = Path("data/douyin")
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)


def douyin_transcript(
    url: str,
    model: str = "tiny",
    format: str = "structure",
    output_dir: str = None
) -> Dict:
    """
    抖音视频语音转文字完整流程
    
    Args:
        url: 抖音视频链接
        model: Whisper 模型大小
        format: 输出格式 (text/structure/json)
        output_dir: 输出目录
    
    Returns:
        包含转录结果的字典
    """
    if output_dir is None:
        output_dir = str(WORKSPACE_DIR)
    
    print("=" * 60)
    print("🎬 抖音视频语音转文字")
    print("=" * 60)
    print(f"📎 URL: {url}")
    print(f"🔧 模型: {model}")
    print(f"📄 格式: {format}")
    print()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("📥 步骤1: 下载视频")
    download_result = download_douyin_video(url, output_dir)
    
    if not download_result.get("success"):
        return {
            "success": False,
            "error": f"视频下载失败: {download_result.get('error')}"
        }
    
    video_path = download_result["video_path"]
    print(f"   ✅ 视频已下载: {video_path}")
    print()
    
    print("🎤 步骤2: 转录音频")
    raw_file = os.path.join(output_dir, f"raw_{timestamp}.txt")
    
    transcribe_result = vt(video_path, model, raw_file)
    
    if not transcribe_result.get("success"):
        return {
            "success": False,
            "error": f"转录失败: {transcribe_result.get('error')}"
        }
    
    raw_text = transcribe_result["text"]
    print(f"   ✅ 转录完成")
    print()
    
    print("✍️ 步骤3: 优化文本")
    output_file = os.path.join(output_dir, f"transcript_{timestamp}.txt")
    refined_text = refine_text(raw_text, format)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(refined_text)
    
    print(f"   ✅ 文本已优化并保存")
    print()
    
    print("=" * 60)
    print("✅ 处理完成!")
    print("=" * 60)
    
    return {
        "success": True,
        "video_path": video_path,
        "transcript_file": output_file,
        "text": refined_text,
        "model": model
    }


def main():
    parser = argparse.ArgumentParser(description="抖音视频语音转文字工具")
    parser.add_argument("url", help="抖音视频URL")
    parser.add_argument("--model", "-m", default="tiny",
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper 模型大小 (默认: tiny)")
    parser.add_argument("--format", "-f", default="structure",
                        choices=["text", "structure", "json"],
                        help="输出格式 (默认: structure)")
    parser.add_argument("--output", "-o", help="输出目录")
    
    args = parser.parse_args()
    
    result = douyin_transcript(
        url=args.url,
        model=args.model,
        format=args.format,
        output_dir=args.output
    )
    
    print("\n📋 最终结果:")
    print("-" * 50)
    if result["success"]:
        print(result["text"])
    else:
        print(f"❌ 错误: {result.get('error')}")


if __name__ == "__main__":
    main()
