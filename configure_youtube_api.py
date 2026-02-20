#!/usr/bin/env python3
"""
YouTube API 配置助手
交互式配置YouTube API密钥
"""

import os
import sys
from pathlib import Path


def configure_youtube_api():
    """交互式配置YouTube API"""
    print("\n" + "🎬"*30)
    print("YouTube API 配置助手")
    print("🎬"*30 + "\n")
    
    print("📋 配置步骤：\n")
    print("1️⃣  访问 Google Cloud Console")
    print("   https://console.cloud.google.com/\n")
    
    print("2️⃣  创建新项目或选择现有项目\n")
    
    print("3️⃣  启用 YouTube Data API v3")
    print("   - 点击左侧菜单 'API和服务' → '库'")
    print("   - 搜索 'YouTube Data API v3'")
    print("   - 点击 '启用'\n")
    
    print("4️⃣  创建 API 密钥")
    print("   - 点击左侧菜单 'API和服务' → '凭据'")
    print("   - 点击 '创建凭据' → 'API密钥'")
    print("   - 复制生成的API密钥\n")
    
    print("5️⃣  （可选）限制 API 密钥")
    print("   - 点击 '限制密钥'")
    print("   - 设置应用程序限制（IP地址或无）")
    print("   - 限制API访问为 'YouTube Data API v3'")
    print("   - 点击 '保存'\n")
    
    print("="*60)
    
    api_key = input("\n请输入你的YouTube API密钥（或按Enter跳过）: ").strip()
    
    if not api_key:
        print("\n❌ 未输入API密钥")
        print("💡 你可以稍后手动编辑 .env 文件")
        return False
    
    env_file = Path(__file__).parent / '.env'
    
    if not env_file.exists():
        print("\n❌ .env 文件不存在")
        print("请先运行项目初始化")
        return False
    
    with open(env_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    updated = False
    new_lines = []
    
    for line in lines:
        if line.startswith('YOUTUBE_API_KEY='):
            new_lines.append(f'YOUTUBE_API_KEY={api_key}\n')
            updated = True
        else:
            new_lines.append(line)
    
    if not updated:
        for i, line in enumerate(new_lines):
            if line.startswith('# YouTube配置'):
                new_lines.insert(i+1, f'YOUTUBE_API_KEY={api_key}\n')
                updated = True
                break
    
    if not updated:
        new_lines.append(f'\n# YouTube配置\nYOUTUBE_API_KEY={api_key}\n')
    
    with open(env_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("\n✅ API密钥已保存到 .env 文件")
    print(f"   密钥: {api_key[:10]}...{api_key[-10:]}")
    
    print("\n🔍 测试API连接...")
    
    try:
        from googleapiclient.discovery import build
        
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        request = youtube.search().list(
            part='snippet',
            q='test',
            maxResults=1,
            type='video'
        )
        response = request.execute()
        
        print("✅ API连接成功！")
        print("\n" + "="*60)
        print("🎉 YouTube API 配置完成！")
        print("="*60)
        print("\n现在你可以使用完整的YouTube API功能了：")
        print("  - 更准确的搜索结果")
        print("  - 更详细的视频信息")
        print("  - 更高的搜索配额")
        print("\n运行测试: python test_youtube_api.py")
        return True
        
    except Exception as e:
        print(f"❌ API连接失败: {e}")
        print("\n请检查：")
        print("  1. API密钥是否正确")
        print("  2. YouTube Data API v3 是否已启用")
        print("  3. API密钥权限设置")
        return False


def show_quota_info():
    """显示配额信息"""
    print("\n" + "="*60)
    print("📊 YouTube API 配额信息")
    print("="*60)
    print("\n默认配额：")
    print("  • 每日配额: 10,000 单位/天")
    print("  • 搜索操作: 100 单位/次")
    print("  • 视频详情: 1 单位/次")
    print("\n估算使用量：")
    print("  • 每天可搜索约 100 次")
    print("  • 每天可获取约 10,000 个视频详情")
    print("\n申请更高配额：")
    print("  https://forms.gle/HGf7nUvXPyvYvM5H9")
    print("="*60)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--quota':
        show_quota_info()
    else:
        configure_youtube_api()
