"""
YouTube视频智能体
功能：搜索、分析、总结YouTube视频内容
"""

import os
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain_zhipu import ChatZhipuAI

from core.config import settings
from utils.logger import logger


class YouTubeAgent:
    """YouTube视频智能体"""
    
    def __init__(self):
        self.llm = ChatZhipuAI(
            model=settings.ZHIPU_MODEL,
            temperature=0.7,
            api_key=settings.ZHIPU_API_KEY
        )
        self.output_dir = Path("data/youtube")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.tools = self._create_tools()
        logger.info("YouTube Agent 初始化完成")
    
    def _create_tools(self) -> List[Tool]:
        """创建工具集"""
        return [
            Tool(
                name="search_youtube",
                description="搜索YouTube视频，支持关键词、频道、时长等筛选",
                func=self._search_youtube
            ),
            Tool(
                name="get_video_details",
                description="获取视频详细信息，包括播放量、点赞数、评论数等",
                func=self._get_video_details
            ),
            Tool(
                name="get_video_transcript",
                description="获取视频字幕/转录文本",
                func=self._get_video_transcript
            ),
            Tool(
                name="summarize_video",
                description="总结视频内容，支持全文总结和精炼要点",
                func=self._summarize_video
            ),
            Tool(
                name="save_video_data",
                description="保存视频数据到文件",
                func=self._save_video_data
            )
        ]
    
    def _search_youtube(
        self,
        query: str,
        max_results: int = 10,
        order: str = "viewCount",
        video_duration: Optional[str] = None,
        published_after: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        搜索YouTube视频
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
            order: 排序方式 (viewCount, relevance, date, rating)
            video_duration: 视频时长筛选 (short, medium, long)
            published_after: 发布日期筛选 (YYYY-MM-DD)
        
        Returns:
            搜索结果字典
        """
        logger.info(f"搜索YouTube视频: {query}")
        
        try:
            from youtube_search import YoutubeSearch
            
            results = YoutubeSearch(
                query,
                max_results=max_results
            ).to_dict()
            
            videos = []
            for video in results:
                video_data = {
                    "video_id": video.get("id", ""),
                    "title": video.get("title", ""),
                    "url": f"https://www.youtube.com{video.get('url_suffix', '')}",
                    "thumbnail": video.get("thumbnails", [{}])[0] if video.get("thumbnails") else "",
                    "channel": video.get("channel", ""),
                    "channel_url": f"https://www.youtube.com{video.get('channel_url_suffix', '')}",
                    "views": self._parse_views(video.get("views", "0")),
                    "duration": video.get("duration", ""),
                    "published": video.get("publish_time", ""),
                    "description": video.get("description", "")
                }
                videos.append(video_data)
            
            if order == "viewCount":
                videos.sort(key=lambda x: x["views"], reverse=True)
            
            logger.info(f"找到 {len(videos)} 个视频")
            return {
                "success": True,
                "query": query,
                "total_results": len(videos),
                "videos": videos,
                "search_params": {
                    "max_results": max_results,
                    "order": order,
                    "video_duration": video_duration,
                    "published_after": published_after
                }
            }
            
        except ImportError:
            logger.warning("youtube_search 未安装，使用模拟数据")
            return self._mock_search(query, max_results)
        except Exception as e:
            logger.error(f"搜索失败: {e}")
            return {"success": False, "error": str(e)}
    
    def _get_video_details(self, video_id: str) -> Dict[str, Any]:
        """
        获取视频详细信息
        
        Args:
            video_id: YouTube视频ID
        
        Returns:
            视频详细信息
        """
        logger.info(f"获取视频详情: {video_id}")
        
        try:
            import yt_dlp
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(
                    f"https://www.youtube.com/watch?v={video_id}",
                    download=False
                )
                
                details = {
                    "video_id": video_id,
                    "title": info.get("title", ""),
                    "description": info.get("description", ""),
                    "duration": info.get("duration", 0),
                    "view_count": info.get("view_count", 0),
                    "like_count": info.get("like_count", 0),
                    "comment_count": info.get("comment_count", 0),
                    "channel": info.get("channel", ""),
                    "channel_id": info.get("channel_id", ""),
                    "channel_url": info.get("channel_url", ""),
                    "channel_follower_count": info.get("channel_follower_count", 0),
                    "upload_date": info.get("upload_date", ""),
                    "categories": info.get("categories", []),
                    "tags": info.get("tags", []),
                    "thumbnail": info.get("thumbnail", ""),
                    "url": f"https://www.youtube.com/watch?v={video_id}"
                }
                
                logger.info(f"获取视频详情成功: {details['title']}")
                return {"success": True, "details": details}
                
        except ImportError:
            logger.warning("yt_dlp 未安装，返回基本信息")
            return {
                "success": True,
                "details": {
                    "video_id": video_id,
                    "url": f"https://www.youtube.com/watch?v={video_id}"
                }
            }
        except Exception as e:
            logger.error(f"获取视频详情失败: {e}")
            return {"success": False, "error": str(e)}
    
    def _list_available_transcripts(self, video_id: str) -> Dict[str, Any]:
        """
        列出视频可用的字幕语言
        
        Args:
            video_id: YouTube视频ID
        
        Returns:
            可用字幕语言列表
        """
        logger.info(f"列出可用字幕语言: {video_id}")
        
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            
            api = YouTubeTranscriptApi()
            transcript_list = api.list(video_id)
            
            available_languages = []
            
            for transcript in transcript_list:
                lang_code = transcript.language_code
                lang_name = transcript.language
                is_generated = transcript.is_generated
                is_translatable = transcript.is_translatable
                
                available_languages.append({
                    "code": lang_code,
                    "name": lang_name,
                    "is_generated": is_generated,
                    "is_translatable": is_translatable
                })
            
            logger.info(f"找到 {len(available_languages)} 种可用字幕语言")
            return {
                "success": True,
                "video_id": video_id,
                "languages": available_languages
            }
            
        except Exception as e:
            logger.error(f"列出字幕语言失败: {e}")
            return {"success": False, "error": str(e)}
    
    def _get_video_transcript(
        self, 
        video_id: str, 
        language: str = "en",
        auto_sentence_break: bool = True
    ) -> Dict[str, Any]:
        """
        获取视频字幕/转录文本
        
        Args:
            video_id: YouTube视频ID
            language: 字幕语言代码 (en, zh-CN, zh-TW等)
            auto_sentence_break: 是否自动断句
        
        Returns:
            转录文本
        """
        logger.info(f"获取视频字幕: {video_id}, 语言: {language}")
        
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            
            api = YouTubeTranscriptApi()
            
            language_map = {
                "中文": ["zh-CN", "zh-Hans", "zh-TW", "zh-Hant", "zh"],
                "英文": ["en", "en-US", "en-GB"],
                "英文自动": ["en"],
                "中文繁体": ["zh-TW", "zh-Hant"],
                "中文简体": ["zh-CN", "zh-Hans"]
            }
            
            if language in language_map:
                lang_codes = language_map[language]
            else:
                lang_codes = [language]
            
            transcript_list = api.fetch(video_id, lang_codes)
            
            raw_text = " ".join([item.text for item in transcript_list])
            
            transcript_with_timestamps = [
                {
                    "start": item.start,
                    "duration": getattr(item, 'duration', 0),
                    "text": item.text
                }
                for item in transcript_list
            ]
            
            if auto_sentence_break:
                full_text = self._auto_sentence_break(raw_text)
            else:
                full_text = raw_text
            
            detected_lang = self._detect_language(full_text[:500])
            
            logger.info(f"获取字幕成功，长度: {len(full_text)}, 语言: {detected_lang}")
            return {
                "success": True,
                "video_id": video_id,
                "full_text": full_text,
                "raw_text": raw_text,
                "transcript": transcript_with_timestamps,
                "language": detected_lang,
                "language_code": lang_codes[0] if lang_codes else language
            }
            
        except ImportError:
            logger.warning("youtube_transcript_api 未安装")
            return {"success": False, "error": "youtube_transcript_api 未安装"}
        except Exception as e:
            logger.error(f"获取字幕失败: {e}")
            return {"success": False, "error": str(e)}
    
    def _auto_sentence_break(self, text: str) -> str:
        """
        自动断句处理
        
        Args:
            text: 原始文本
        
        Returns:
            断句后的文本
        """
        import re
        
        text = re.sub(r'\s+', ' ', text)
        
        text = re.sub(r'([.!?])\s+', r'\1\n\n', text)
        
        text = re.sub(r'([。！？])', r'\1\n\n', text)
        
        text = re.sub(r'([,，])\s*', r'\1 ', text)
        
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def _detect_language(self, text: str) -> str:
        """
        检测文本语言
        
        Args:
            text: 文本内容
        
        Returns:
            语言名称
        """
        chinese_chars = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
        total_chars = len(text.replace(' ', ''))
        
        if total_chars > 0 and chinese_chars / total_chars > 0.3:
            return "中文"
        else:
            return "英文"
    
    def _summarize_video(
        self,
        transcript: str,
        video_title: str = "",
        summary_type: str = "concise"
    ) -> Dict[str, Any]:
        """
        总结视频内容
        
        Args:
            transcript: 视频转录文本
            video_title: 视频标题
            summary_type: 总结类型 (full: 全文总结, concise: 精炼要点)
        
        Returns:
            总结结果
        """
        logger.info(f"总结视频内容: {video_title}, 类型: {summary_type}")
        
        if not transcript:
            return {"success": False, "error": "转录文本为空"}
        
        if summary_type == "full":
            prompt = f"""请对以下YouTube视频内容进行详细的全文总结。

视频标题：{video_title}

视频内容：
{transcript[:8000]}

请提供：
1. 视频主要内容概述
2. 关键观点和论据
3. 重要细节和数据
4. 结论和建议

请用中文回答。"""
        else:
            prompt = f"""请对以下YouTube视频内容进行精炼要点总结。

视频标题：{video_title}

视频内容：
{transcript[:8000]}

请提供：
1. 核心主题（1-2句话）
2. 关键要点（3-5个要点）
3. 重要结论（1-2句话）

请用中文回答，简洁明了。"""
        
        try:
            response = self.llm.invoke(prompt)
            summary = response.content
            
            logger.info("视频总结完成")
            return {
                "success": True,
                "video_title": video_title,
                "summary_type": summary_type,
                "summary": summary,
                "transcript_length": len(transcript)
            }
        except Exception as e:
            logger.error(f"总结失败: {e}")
            return {"success": False, "error": str(e)}
    
    def _save_video_data(
        self,
        video_data: Dict[str, Any],
        filename: Optional[str] = None,
        format: str = "json"
    ) -> Dict[str, Any]:
        """
        保存视频数据到文件
        
        Args:
            video_data: 视频数据
            filename: 文件名（不含扩展名）
            format: 保存格式 (json, markdown, both)
        
        Returns:
            保存结果
        """
        logger.info(f"保存视频数据: {filename}")
        
        if not filename:
            video_id = video_data.get("video_id", "unknown")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"video_{video_id}_{timestamp}"
        
        saved_files = []
        
        try:
            if format in ["json", "both"]:
                json_path = self.output_dir / f"{filename}.json"
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(video_data, f, ensure_ascii=False, indent=2)
                saved_files.append(str(json_path))
                logger.info(f"JSON文件已保存: {json_path}")
            
            if format in ["markdown", "both"]:
                md_path = self.output_dir / f"{filename}.md"
                markdown_content = self._generate_markdown_report(video_data)
                with open(md_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                saved_files.append(str(md_path))
                logger.info(f"Markdown文件已保存: {md_path}")
            
            return {
                "success": True,
                "saved_files": saved_files,
                "output_dir": str(self.output_dir)
            }
            
        except Exception as e:
            logger.error(f"保存失败: {e}")
            return {"success": False, "error": str(e)}
    
    def _generate_markdown_report(self, video_data: Dict[str, Any]) -> str:
        """生成Markdown格式的报告"""
        md = f"""# YouTube视频分析报告

## 基本信息

- **视频标题**: {video_data.get('title', 'N/A')}
- **视频ID**: {video_data.get('video_id', 'N/A')}
- **视频链接**: {video_data.get('url', 'N/A')}
- **频道**: {video_data.get('channel', 'N/A')}
- **发布日期**: {video_data.get('upload_date', video_data.get('published', 'N/A'))}
- **时长**: {video_data.get('duration', 'N/A')}

## 数据统计

- **播放量**: {self._format_number(video_data.get('view_count', video_data.get('views', 0)))}
- **点赞数**: {self._format_number(video_data.get('like_count', 0))}
- **评论数**: {self._format_number(video_data.get('comment_count', 0))}
- **频道订阅数**: {self._format_number(video_data.get('channel_follower_count', 0))}

## 视频描述

{video_data.get('description', '无描述')}

## 内容总结

{video_data.get('summary', '暂无总结')}

## 关键要点

"""
        key_points = video_data.get('key_points', [])
        if key_points:
            for i, point in enumerate(key_points, 1):
                md += f"{i}. {point}\n"
        else:
            md += "暂无关键要点\n"
        
        md += f"""
## 元数据

- **分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **标签**: {', '.join(video_data.get('tags', [])) or '无'}
- **分类**: {', '.join(video_data.get('categories', [])) or '无'}

---
*此报告由 Zzy_Personal_Agent YouTube智能体自动生成*
"""
        return md
    
    def _parse_views(self, views_str: str) -> int:
        """解析播放量字符串"""
        try:
            views_str = views_str.replace(",", "").replace("次观看", "").replace("views", "").strip()
            if "万" in views_str:
                return int(float(views_str.replace("万", "")) * 10000)
            elif "M" in views_str:
                return int(float(views_str.replace("M", "")) * 1000000)
            elif "K" in views_str:
                return int(float(views_str.replace("K", "")) * 1000)
            return int(views_str)
        except:
            return 0
    
    def _format_number(self, num) -> str:
        """格式化数字显示"""
        if num is None:
            return "N/A"
        if not isinstance(num, (int, float)):
            return str(num)
        if num >= 10000000:
            return f"{num/10000000:.1f}千万"
        elif num >= 10000:
            return f"{num/10000:.1f}万"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        return str(num)
    
    def _mock_search(self, query: str, max_results: int) -> Dict[str, Any]:
        """模拟搜索结果（用于测试）"""
        return {
            "success": True,
            "query": query,
            "total_results": 0,
            "videos": [],
            "message": "请安装 youtube_search 库: pip install youtube-search"
        }
    
    async def run(
        self,
        query: str,
        max_results: int = 5,
        get_transcript: bool = True,
        summary_type: str = "concise",
        save_format: str = "both"
    ) -> Dict[str, Any]:
        """
        运行完整的YouTube视频分析流程
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
            get_transcript: 是否获取字幕
            summary_type: 总结类型
            save_format: 保存格式
        
        Returns:
            完整分析结果
        """
        logger.info(f"开始YouTube视频分析: {query}")
        
        results = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "videos": []
        }
        
        search_result = self._search_youtube(query, max_results)
        if not search_result.get("success"):
            return {"success": False, "error": "搜索失败", "details": search_result}
        
        videos = search_result.get("videos", [])
        
        for i, video in enumerate(videos[:max_results], 1):
            logger.info(f"处理视频 {i}/{len(videos)}: {video['title']}")
            
            video_data = video.copy()
            
            details_result = self._get_video_details(video["video_id"])
            if details_result.get("success"):
                video_data.update(details_result.get("details", {}))
            
            if get_transcript:
                transcript_result = self._get_video_transcript(video["video_id"])
                if transcript_result.get("success"):
                    video_data["transcript"] = transcript_result.get("full_text", "")
                    video_data["transcript_data"] = transcript_result.get("transcript", [])
                    
                    summary_result = self._summarize_video(
                        video_data["transcript"],
                        video_data["title"],
                        summary_type
                    )
                    if summary_result.get("success"):
                        video_data["summary"] = summary_result.get("summary", "")
            
            save_result = self._save_video_data(
                video_data,
                f"video_{video['video_id']}",
                save_format
            )
            video_data["saved_files"] = save_result.get("saved_files", [])
            
            results["videos"].append(video_data)
        
        self._save_video_data(
            results,
            f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "json"
        )
        
        logger.info(f"YouTube视频分析完成，共处理 {len(results['videos'])} 个视频")
        return {"success": True, **results}
    
    def interactive_search(self) -> None:
        """交互式搜索模式"""
        print("\n" + "="*50)
        print("YouTube视频智能体 - 交互式搜索")
        print("="*50 + "\n")
        
        query = input("请输入搜索关键词: ").strip()
        if not query:
            print("搜索关键词不能为空")
            return
        
        try:
            max_results = int(input("最大结果数 (默认5): ").strip() or "5")
        except ValueError:
            max_results = 5
        
        summary_type = input("总结类型 (full/concise, 默认concise): ").strip() or "concise"
        
        print(f"\n正在搜索: {query}...")
        
        import asyncio
        result = asyncio.run(self.run(
            query=query,
            max_results=max_results,
            summary_type=summary_type
        ))
        
        if result.get("success"):
            print(f"\n✅ 分析完成！共处理 {len(result['videos'])} 个视频")
            print(f"📁 数据已保存到: {self.output_dir}")
            
            for i, video in enumerate(result['videos'], 1):
                print(f"\n{i}. {video['title']}")
                print(f"   播放量: {self._format_number(video.get('view_count', video.get('views', 0)))}")
                print(f"   频道: {video.get('channel', 'N/A')}")
                if video.get('summary'):
                    print(f"   总结: {video['summary'][:100]}...")
        else:
            print(f"\n❌ 分析失败: {result.get('error')}")


if __name__ == "__main__":
    agent = YouTubeAgent()
    agent.interactive_search()
