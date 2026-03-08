#!/usr/bin/env python3
"""
视频语音转文字工具
使用 OpenAI Whisper 进行语音识别
"""

import os
import sys
import json
import argparse
import subprocess
import tempfile
from pathlib import Path


def extract_audio(video_path: str, output_path: str = None) -> str:
    """使用 ffmpeg 从视频中提取音频"""
    if output_path is None:
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, "audio.wav")
    
    print(f"🎵 正在提取音频...")
    
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        "-y",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ 音频提取失败: {result.stderr}")
        return None
    
    print(f"✅ 音频提取成功: {output_path}")
    return output_path


def transcribe_audio(audio_path: str, model: str = "tiny", language: str = "zh") -> str:
    """使用 Whisper 转录音频"""
    print(f"🎤 正在使用 Whisper {model} 模型转录...")
    
    try:
        import whisper
    except ImportError:
        print("📦 正在安装 openai-whisper...")
        subprocess.run([sys.executable, "-m", "pip", "install", "openai-whisper"], check=True)
        import whisper
    
    try:
        model_obj = whisper.load_model(model)
        result = model_obj.transcribe(audio_path, language=language)
        return result["text"]
    except Exception as e:
        print(f"❌ 转录失败: {e}")
        return None


def video_to_text(video_path: str, model: str = "tiny", output_file: str = None) -> dict:
    """
    将视频转换为文字
    
    Args:
        video_path: 视频文件路径
        model: Whisper 模型大小 (tiny/base/small/medium/large)
        output_file: 输出文件路径
    
    Returns:
        包含转录结果的字典
    """
    if not os.path.exists(video_path):
        print(f"❌ 文件不存在: {video_path}")
        return {"success": False, "error": "File not found"}
    
    audio_path = extract_audio(video_path)
    if not audio_path:
        return {"success": False, "error": "Audio extraction failed"}
    
    text = transcribe_audio(audio_path, model)
    
    if text:
        print(f"✅ 转录完成")
        
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"📝 已保存到: {output_file}")
        
        os.remove(audio_path)
        
        return {
            "success": True,
            "text": text,
            "model": model
        }
    else:
        return {"success": False, "error": "Transcription failed"}


def main():
    parser = argparse.ArgumentParser(description="视频语音转文字工具")
    parser.add_argument("video", help="视频文件路径或URL")
    parser.add_argument("--model", "-m", default="tiny", 
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper 模型大小 (默认: tiny)")
    parser.add_argument("--language", "-l", default="zh",
                        help="语言代码 (默认: zh)")
    parser.add_argument("--output", "-o", help="输出文件路径")
    
    args = parser.parse_args()
    
    video_path = args.video
    
    if video_path.startswith("http"):
        print("📥 检测到URL，正在下载...")
        from douyin_downloader import download_douyin_video
        result = download_douyin_video(video_path)
        if result.get("success"):
            video_path = result["video_path"]
        else:
            print(f"❌ 下载失败: {result.get('error')}")
            return
    
    result = video_to_text(video_path, args.model, args.output)
    
    print("\n" + "=" * 50)
    if result["success"]:
        print("📝 转录结果:")
        print(result["text"])
    else:
        print(f"❌ 转录失败: {result.get('error')}")


if __name__ == "__main__":
    main()
