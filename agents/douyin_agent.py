#!/usr/bin/env python3
"""
抖音视频智能体
功能：下载抖音视频并提取语音转录文字
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_core.tools import Tool

from scripts.tools.douyin_transcript import douyin_transcript
from utils.logger import logger


class DouyinAgent:
    """抖音视频智能体"""
    
    def __init__(self):
        self.output_dir = Path("data/douyin")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.tools = self._create_tools()
        logger.info("Douyin Agent 初始化完成")
    
    def _create_tools(self) -> List[Tool]:
        """创建工具集"""
        return [
            Tool(
                name="douyin_transcribe",
                description="""将抖音视频链接转换为文字稿。
                输入：抖音视频链接
                功能：自动下载视频、提取音频、使用Whisper转录、优化文本
                输出格式：结构化文本，包含段落划分和关键观点""",
                func=self._transcribe_douyin
            ),
            Tool(
                name="douyin_download",
                description="""下载抖音视频到本地。
                输入：抖音视频链接
                输出：视频文件路径""",
                func=self._download_douyin
            )
        ]
    
    def _transcribe_douyin(self, url: str, model: str = "tiny", format: str = "structure") -> str:
        """
        转录抖音视频
        
        Args:
            url: 抖音视频链接
            model: Whisper 模型大小
            format: 输出格式
        
        Returns:
            转录文本
        """
        logger.info(f"转录抖音视频: {url}")
        
        try:
            result = douyin_transcript(
                url=url,
                model=model,
                format=format,
                output_dir=str(self.output_dir)
            )
            
            if result.get("success"):
                return result["text"]
            else:
                return f"转录失败: {result.get('error')}"
                
        except Exception as e:
            logger.error(f"转录出错: {e}")
            return f"转录出错: {str(e)}"
    
    def _download_douyin(self, url: str) -> str:
        """
        下载抖音视频
        
        Args:
            url: 抖音视频链接
        
        Returns:
            下载结果信息
        """
        logger.info(f"下载抖音视频: {url}")
        
        try:
            from tools.douyin_downloader import download_douyin_video
            
            result = download_douyin_video(url, str(self.output_dir))
            
            if result.get("success"):
                return json.dumps({
                    "success": True,
                    "video_path": result["video_path"],
                    "file_size": result.get("file_size", 0)
                }, ensure_ascii=False, indent=2)
            else:
                return json.dumps({
                    "success": False,
                    "error": result.get("error")
                }, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"下载出错: {e}")
            return json.dumps({
                "success": False,
                "error": str(e)
            }, ensure_ascii=False, indent=2)


douyin_agent = DouyinAgent()
douyin_tools = douyin_agent.tools
