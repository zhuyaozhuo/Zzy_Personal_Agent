"""
YouTube服务模块
提供YouTube API集成功能
"""

import os
from typing import Optional, Dict, Any, List
from datetime import datetime
import json

from utils.logger import logger


class YouTubeService:
    """YouTube服务类"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY")
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    async def search_videos(
        self,
        query: str,
        max_results: int = 10,
        order: str = "viewCount",
        video_duration: Optional[str] = None,
        region_code: str = "US"
    ) -> Dict[str, Any]:
        """
        使用YouTube Data API搜索视频
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
            order: 排序方式
            video_duration: 视频时长
            region_code: 地区代码
        
        Returns:
            搜索结果
        """
        if not self.api_key:
            logger.warning("YouTube API Key 未配置，使用备用方案")
            return await self._fallback_search(query, max_results)
        
        try:
            import aiohttp
            
            params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": max_results,
                "order": order,
                "key": self.api_key,
                "regionCode": region_code
            }
            
            if video_duration:
                params["videoDuration"] = video_duration
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/search",
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._process_search_results(data)
                    else:
                        error = await response.text()
                        logger.error(f"YouTube API 错误: {error}")
                        return {"success": False, "error": error}
                        
        except Exception as e:
            logger.error(f"搜索失败: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_video_statistics(
        self,
        video_ids: List[str]
    ) -> Dict[str, Any]:
        """
        获取视频统计数据
        
        Args:
            video_ids: 视频ID列表
        
        Returns:
            统计数据
        """
        if not self.api_key:
            return {"success": False, "error": "API Key 未配置"}
        
        try:
            import aiohttp
            
            params = {
                "part": "statistics,contentDetails,snippet",
                "id": ",".join(video_ids),
                "key": self.api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/videos",
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._process_video_details(data)
                    else:
                        error = await response.text()
                        return {"success": False, "error": error}
                        
        except Exception as e:
            logger.error(f"获取统计数据失败: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_channel_info(
        self,
        channel_id: str
    ) -> Dict[str, Any]:
        """
        获取频道信息
        
        Args:
            channel_id: 频道ID
        
        Returns:
            频道信息
        """
        if not self.api_key:
            return {"success": False, "error": "API Key 未配置"}
        
        try:
            import aiohttp
            
            params = {
                "part": "statistics,snippet,brandingSettings",
                "id": channel_id,
                "key": self.api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/channels",
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._process_channel_info(data)
                    else:
                        error = await response.text()
                        return {"success": False, "error": error}
                        
        except Exception as e:
            logger.error(f"获取频道信息失败: {e}")
            return {"success": False, "error": str(e)}
    
    async def _fallback_search(
        self,
        query: str,
        max_results: int
    ) -> Dict[str, Any]:
        """备用搜索方案（不使用API Key）"""
        try:
            from youtube_search import YoutubeSearch
            
            results = YoutubeSearch(query, max_results=max_results).to_dict()
            
            videos = []
            for item in results:
                videos.append({
                    "video_id": item.get("id", ""),
                    "title": item.get("title", ""),
                    "url": f"https://www.youtube.com{item.get('url_suffix', '')}",
                    "thumbnail": item.get("thumbnails", [{}])[0] if item.get("thumbnails") else "",
                    "channel": item.get("channel", ""),
                    "views": item.get("views", "0"),
                    "duration": item.get("duration", ""),
                    "published": item.get("publish_time", ""),
                    "description": item.get("description", "")[:200] if item.get("description") else ""
                })
            
            return {
                "success": True,
                "videos": videos,
                "total_results": len(videos),
                "source": "youtube_search"
            }
            
        except ImportError:
            return {
                "success": False,
                "error": "请安装 youtube-search: pip install youtube-search",
                "videos": []
            }
        except Exception as e:
            return {"success": False, "error": str(e), "videos": []}
    
    def _process_search_results(self, data: Dict) -> Dict[str, Any]:
        """处理搜索结果"""
        videos = []
        
        for item in data.get("items", []):
            snippet = item.get("snippet", {})
            video_id = item.get("id", {}).get("videoId", "")
            
            videos.append({
                "video_id": video_id,
                "title": snippet.get("title", ""),
                "description": snippet.get("description", ""),
                "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
                "channel": snippet.get("channelTitle", ""),
                "channel_id": snippet.get("channelId", ""),
                "published_at": snippet.get("publishedAt", ""),
                "url": f"https://www.youtube.com/watch?v={video_id}"
            })
        
        return {
            "success": True,
            "videos": videos,
            "total_results": len(videos),
            "page_info": data.get("pageInfo", {}),
            "source": "youtube_api"
        }
    
    def _process_video_details(self, data: Dict) -> Dict[str, Any]:
        """处理视频详情"""
        videos = {}
        
        for item in data.get("items", []):
            video_id = item.get("id", "")
            stats = item.get("statistics", {})
            content = item.get("contentDetails", {})
            snippet = item.get("snippet", {})
            
            videos[video_id] = {
                "video_id": video_id,
                "title": snippet.get("title", ""),
                "view_count": int(stats.get("viewCount", 0)),
                "like_count": int(stats.get("likeCount", 0)),
                "comment_count": int(stats.get("commentCount", 0)),
                "duration": content.get("duration", ""),
                "channel": snippet.get("channelTitle", ""),
                "channel_id": snippet.get("channelId", ""),
                "published_at": snippet.get("publishedAt", ""),
                "tags": snippet.get("tags", []),
                "category_id": snippet.get("categoryId", "")
            }
        
        return {"success": True, "videos": videos}
    
    def _process_channel_info(self, data: Dict) -> Dict[str, Any]:
        """处理频道信息"""
        items = data.get("items", [])
        
        if not items:
            return {"success": False, "error": "频道未找到"}
        
        item = items[0]
        stats = item.get("statistics", {})
        snippet = item.get("snippet", {})
        
        return {
            "success": True,
            "channel": {
                "channel_id": item.get("id", ""),
                "title": snippet.get("title", ""),
                "description": snippet.get("description", ""),
                "subscriber_count": int(stats.get("subscriberCount", 0)),
                "view_count": int(stats.get("viewCount", 0)),
                "video_count": int(stats.get("videoCount", 0)),
                "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
                "published_at": snippet.get("publishedAt", "")
            }
        }


class TranscriptService:
    """字幕服务类"""
    
    @staticmethod
    async def get_transcript(
        video_id: str,
        languages: List[str] = None
    ) -> Dict[str, Any]:
        """
        获取视频字幕
        
        Args:
            video_id: 视频ID
            languages: 语言优先级列表
        
        Returns:
            字幕数据
        """
        if languages is None:
            languages = ['zh-CN', 'zh-TW', 'en']
        
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            
            transcript_list = YouTubeTranscriptApi.get_transcript(
                video_id,
                languages=languages
            )
            
            full_text = " ".join([item["text"] for item in transcript_list])
            
            segments = [
                {
                    "start": item["start"],
                    "duration": item.get("duration", 0),
                    "text": item["text"]
                }
                for item in transcript_list
            ]
            
            return {
                "success": True,
                "video_id": video_id,
                "full_text": full_text,
                "segments": segments,
                "language": languages[0] if transcript_list else "unknown"
            }
            
        except ImportError:
            return {
                "success": False,
                "error": "请安装 youtube-transcript-api: pip install youtube-transcript-api"
            }
        except Exception as e:
            logger.error(f"获取字幕失败: {e}")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def format_transcript_with_timestamps(
        segments: List[Dict],
        interval: int = 60
    ) -> str:
        """
        格式化带时间戳的字幕
        
        Args:
            segments: 字幕片段列表
            interval: 时间间隔（秒）
        
        Returns:
            格式化后的文本
        """
        formatted = []
        current_time = 0
        
        for segment in segments:
            start = segment["start"]
            
            if start >= current_time + interval:
                minutes = int(start // 60)
                seconds = int(start % 60)
                formatted.append(f"\n[{minutes:02d}:{seconds:02d}]")
                current_time = start
            
            formatted.append(segment["text"])
        
        return " ".join(formatted)
