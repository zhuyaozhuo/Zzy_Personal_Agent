#!/usr/bin/env python3
"""
Tavily 搜索工具
集成 Tavily 搜索引擎进行实时信息搜索
"""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any

from dotenv import load_dotenv

project_root = Path(__file__).parent.parent.parent
load_dotenv(project_root / ".env")

from langchain_core.tools import Tool
from tavily import TavilyClient


class TavilySearchTool:
    """Tavily 搜索工具类"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("需要设置 TAVILY_API_KEY 环境变量")
        
        self.client = TavilyClient(api_key=self.api_key)
        self.tools = self._create_tools()
    
    def _create_tools(self) -> List[Tool]:
        """创建工具集"""
        return [
            Tool(
                name="tavily_search",
                description="""Tavily 实时搜索引擎。
                用于搜索最新新闻、实时信息、百科知识等。
                输入：搜索关键词
                返回：相关搜索结果摘要""",
                func=self.search
            ),
            Tool(
                name="tavily_search_deep",
                description="""Tavily 深度搜索。
                进行更详细的搜索，获取更全面的信息。
                适用于需要深入了解某个主题的场景。""",
                func=self.search_deep
            )
        ]
    
    def search(self, query: str, max_results: int = 5) -> str:
        """
        快速搜索
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
        
        Returns:
            搜索结果
        """
        try:
            results = self.client.search(
                query=query,
                max_results=max_results
            )
            
            output = f"🔍 搜索结果: {query}\n\n"
            
            for i, result in enumerate(results.get("results", []), 1):
                title = result.get("title", "无标题")
                url = result.get("url", "")
                content = result.get("content", "")[:200]
                
                output += f"{i}. {title}\n"
                output += f"   {content}...\n"
                output += f"   🔗 {url}\n\n"
            
            return output
            
        except Exception as e:
            return f"搜索出错: {str(e)}"
    
    def search_deep(self, query: str, max_results: int = 10) -> str:
        """
        深度搜索
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
        
        Returns:
            搜索结果
        """
        try:
            results = self.client.search(
                query=query,
                max_results=max_results,
                include_answer=True,
                include_raw_content=True
            )
            
            output = f"🔍 深度搜索: {query}\n\n"
            
            if results.get("answer"):
                output += f"📝 答案摘要:\n{results['answer']}\n\n"
            
            output += "📋 搜索结果:\n"
            for i, result in enumerate(results.get("results", []), 1):
                title = result.get("title", "无标题")
                url = result.get("url", "")
                content = result.get("content", "")[:300]
                
                output += f"\n{i}. {title}\n"
                output += f"   {content}...\n"
                output += f"   🔗 {url}\n"
            
            return output
            
        except Exception as e:
            return f"搜索出错: {str(e)}"


def get_tavily_tools(api_key: str = None) -> List[Tool]:
    """获取 Tavily 搜索工具"""
    tool = TavilySearchTool(api_key)
    return tool.tools


tavily_search_tool = None

def init_tavily(api_key: str = None) -> List[Tool]:
    """初始化 Tavily 工具"""
    global tavily_search_tool
    tavily_search_tool = TavilySearchTool(api_key)
    return tavily_search_tool.tools
