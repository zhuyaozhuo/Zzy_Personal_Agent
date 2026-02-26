#!/usr/bin/env python3
"""
测试 LLM 连接的简单脚本
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.config import settings


def test_direct_connection():
    """直接使用 zhipuai SDK 测试连接"""
    try:
        from zhipuai import ZhipuAI
        
        print("="*60)
        print("测试 1: 直接使用 zhipuai SDK")
        print("="*60)
        
        client = ZhipuAI(api_key=settings.ZHIPU_API_KEY)
        
        print(f"API Key: {settings.ZHIPU_API_KEY[:10]}...")
        print(f"Model: {settings.ZHIPU_MODEL}")
        
        response = client.chat.completions.create(
            model=settings.ZHIPU_MODEL,
            messages=[
                {"role": "user", "content": "你好，请回复一句话。"}
            ],
            temperature=0.3
        )
        
        print("\n✅ 连接成功！")
        print(f"响应: {response.choices[0].message.content}")
        return True
        
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install zhipuai")
        return False
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_langchain_zhipu():
    """测试 langchain_zhipu 包"""
    try:
        print("\n" + "="*60)
        print("测试 2: 使用 langchain_zhipu")
        print("="*60)
        
        from langchain_zhipu import ChatZhipuAI
        from langchain_core.messages import HumanMessage
        
        print(f"API Key: {settings.ZHIPU_API_KEY[:10]}...")
        print(f"Model: {settings.ZHIPU_MODEL}")
        
        llm = ChatZhipuAI(
            model=settings.ZHIPU_MODEL,
            temperature=0.3,
            api_key=settings.ZHIPU_API_KEY
        )
        
        response = llm.invoke([HumanMessage(content="你好，请回复一句话。")])
        
        print("\n✅ 连接成功！")
        print(f"响应: {response.content}")
        return True
        
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install langchain-zhipu")
        return False
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n" + "🚀"*30)
    print("LLM 连接诊断工具")
    print("🚀"*30)
    
    success1 = test_direct_connection()
    success2 = test_langchain_zhipu()
    
    print("\n" + "="*60)
    print("测试结果汇总:")
    print(f"  直接 SDK 测试: {'✅ 通过' if success1 else '❌ 失败'}")
    print(f"  LangChain 测试: {'✅ 通过' if success2 else '❌ 失败'}")
    print("="*60)


if __name__ == "__main__":
    main()
