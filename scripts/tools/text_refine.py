#!/usr/bin/env python3
"""
文本优化工具
对语音转录的原始文本进行优化处理
"""

import re
import json
import argparse
from typing import List, Dict


COMMON_CORRECTIONS = {
    "每人": "美股",
    "货牧斯": "霍尔木兹",
    "跌了": "低了",
    "那个": "那个",
    "然后": "然后",
    "就是": "就是",
    "其实": "其实",
    "可能": "可能",
    "应该": "应该",
    "因为": "因为",
    "所以": "所以",
    "但是": "但是",
    "如果": "如果",
    "虽然": "虽然",
    "不过": "不过",
    "或者": "或者",
    "以及": "以及",
    "对于": "对于",
    "关于": "关于",
    "通过": "通过",
    "进行": "进行",
    "这个": "这个",
    "那个": "那个",
    "什么": "什么",
    "怎么": "怎么",
    "为什么": "为什么",
    "怎么样": "怎么样",
}


def add_punctuation(text: str) -> str:
    """添加标点符号"""
    text = re.sub(r'([^\n]) ([A-Z])', r'\1\n\n\2', text)
    
    text = re.sub(r'([。！？])\s*([^\n])', r'\1\n\2', text)
    
    return text


def correct_common_errors(text: str) -> str:
    """修正常见识别错误"""
    for wrong, correct in COMMON_CORRECTIONS.items():
        text = text.replace(wrong, correct)
    
    text = re.sub(r'\s+', ' ', text)
    
    return text


def split_into_paragraphs(text: str) -> List[str]:
    """将文本分割成段落"""
    paragraphs = []
    
    parts = re.split(r'([。！？\n])', text)
    
    current_para = ""
    for i, part in enumerate(parts):
        current_para += part
        if part in '。！？\n' and len(current_para) > 50:
            paragraphs.append(current_para.strip())
            current_para = ""
    
    if current_para.strip():
        paragraphs.append(current_para.strip())
    
    return paragraphs


def extract_key_points(text: str) -> List[str]:
    """提取关键观点"""
    key_points = []
    
    patterns = [
        r'([^。]*?)是([^。]*?)的',
        r'([^。]*?)说明([^。]*?)了',
        r'([^。]*?)认为([^。]*?)',
        r'([^。]*?)表示([^。]*?)',
        r'([^。]*?)指出([^。]*?)',
        r'重要([^。]*?)是',
        r'关键([^。]*?)是',
        r'首先([^。]*?)',
        r'其次([^。]*?)',
        r'最后([^。]*?)',
    ]
    
    sentences = re.split(r'[。！？\n]', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 10 and len(sentence) < 100:
            key_points.append(sentence)
    
    return key_points[:10]


def refine_text(input_text: str, format: str = "structure") -> str:
    """
    优化文本
    
    Args:
        input_text: 原始转录文本
        format: 输出格式 (text/structure/json)
    
    Returns:
        优化后的文本
    """
    text = correct_common_errors(input_text)
    text = add_punctuation(text)
    
    if format == "text":
        return text
    
    elif format == "structure":
        paragraphs = split_into_paragraphs(text)
        
        output = "📝 文本优化结果\n\n"
        
        for i, para in enumerate(paragraphs, 1):
            output += f"【段落 {i}】\n{para}\n\n"
        
        key_points = extract_key_points(text)
        if key_points:
            output += "💡 关键观点：\n"
            for point in key_points[:5]:
                output += f"• {point}\n"
        
        return output
    
    elif format == "json":
        paragraphs = split_into_paragraphs(text)
        key_points = extract_key_points(text)
        
        result = {
            "original_text": input_text,
            "refined_text": text,
            "paragraphs": paragraphs,
            "key_points": key_points,
            "summary": f"共 {len(paragraphs)} 个段落，{len(key_points)} 个关键观点"
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    return text


def main():
    parser = argparse.ArgumentParser(description="文本优化工具")
    parser.add_argument("input", help="输入文件路径或文本")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--format", "-f", default="structure",
                        choices=["text", "structure", "json"],
                        help="输出格式 (默认: structure)")
    
    args = parser.parse_args()
    
    if os.path.exists(args.input):
        with open(args.input, "r", encoding="utf-8") as f:
            input_text = f.read()
    else:
        input_text = args.input
    
    result = refine_text(input_text, args.format)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"✅ 已保存到: {args.output}")
    else:
        print("\n" + "=" * 50)
        print(result)


if __name__ == "__main__":
    import os
    main()
