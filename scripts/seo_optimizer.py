#!/usr/bin/env python3
"""SEO Optimization Script - Add meta tags to all HTML pages"""

import os
import re

# SEO template for each page type
SEO_TEMPLATES = {
    'index': {
        'title': '诸葛邓炮 - AI助手与自动化工具',
        'description': '诸葛邓炮是您的个人AI助手，提供智能对话、自动化脚本、创意工具等强大功能。帮助您更高效地完成工作和创意任务。',
        'keywords': 'AI助手, 自动化工具, OpenClaw, 人工智能, 智能助手'
    },
    'about': {
        'title': '关于我们 - 诸葛邓炮',
        'description': '了解诸葛邓炮团队，我们致力于用AI技术简化您的工作和生活。',
        'keywords': '团队, 关于我们, AI技术'
    },
    'articles': {
        'title': '文章中心 - 诸葛邓炮',
        'description': '阅读最新的AI技术文章、工具教程和行业见解。',
        'keywords': '文章, AI技术, 教程, 博客'
    },
    'contact': {
        'title': '联系我们 - 诸葛邓炮',
        'description': '有任何问题或建议？请通过各种渠道联系我们。',
        'keywords': '联系, 反馈, 支持'
    },
    'diary': {
        'title': '日记 - 诸葛邓炮',
        'description': '记录AI助手与人类协作的日常，探索智能办公的无限可能。',
        'keywords': '日记, 笔记, AI协作'
    },
    'easyclaw': {
        'title': 'EasyClaw - 诸葛邓炮',
        'description': 'EasyClaw让您轻松使用AI助手，无需复杂配置。',
        'keywords': 'EasyClaw, 简单, 易用'
    },
    'faq': {
        'title': '常见问题 - 诸葛邓炮',
        'description': '查找关于诸葛邓炮的常见问题答案。',
        'keywords': 'FAQ, 问题, 答案, 帮助'
    },
    'footprint': {
        'title': '足迹 - 诸葛邓炮',
        'description': '探索诸葛邓炮在不同领域的应用案例和成果展示。',
        'keywords': '案例, 成果, 展示'
    },
    'insights': {
        'title': '洞察与观点 - 诸葛邓炮',
        'description': 'AI行业洞察、技术趋势和深度分析。',
        'keywords': '洞察, 观点, AI趋势, 技术分析'
    },
    'office': {
        'title': '办公助手 - 诸葛邓炮',
        'description': 'AI驱动的智能办公解决方案，提升团队协作效率。',
        'keywords': '办公, 协作, 效率, 智能办公'
    },
    'openclaw-install': {
        'title': '安装OpenClaw - 诸葛邓炮',
        'description': '详细指南：如何在您的设备上安装和配置OpenClaw。',
        'keywords': '安装, OpenClaw, 配置, 教程'
    },
    'pricing': {
        'title': '定价方案 - 诸葛邓炮',
        'description': '了解诸葛邓炮的订阅计划和价格选项。',
        'keywords': '定价, 价格, 订阅, 计划'
    },
    'radar': {
        'title': 'AI雷达 - 诸葛邓炮',
        'description': '探索最新最热的AI工具和科技动态。',
        'keywords': 'AI雷达, 工具, 科技动态'
    },
    'science': {
        'title': 'AI科学 - 诸葛邓炮',
        'description': '深入了解人工智能的科学原理和技术架构。',
        'keywords': 'AI科学, 技术原理, 架构'
    },
    'skills': {
        'title': '技能中心 - 诸葛邓炮',
        'description': '探索诸葛邓炮的强大技能：语音、图像、代码等。',
        'keywords': '技能, 语音, 图像, 代码'
    },
    'testimonials': {
        'title': '用户评价 - 诸葛邓炮',
        'description': '听听用户如何评价诸葛邓炮。',
        'keywords': '评价, 用户, 推荐'
    }
}

def generate_seo_tags(page_name, title=None, description=None, keywords=None):
    """Generate SEO meta tags"""
    template = SEO_TEMPLATES.get(page_name.lower().replace('.html', ''), {})
    
    final_title = title or template.get('title', '诸葛邓炮')
    final_desc = description or template.get('description', '诸葛邓炮 - 您的AI助手')
    final_keywords = keywords or template.get('keywords', 'AI助手, OpenClaw')
    
    return f'''
    <!-- SEO Meta Tags -->
    <meta name="description" content="{final_desc}">
    <meta name="keywords" content="{final_keywords}">
    <meta name="author" content="ZhugeDengpao Team">
    <meta name="robots" content="index, follow">
    
    <!-- Open Graph Tags -->
    <meta property="og:title" content="{final_title}">
    <meta property="og:description" content="{final_desc}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://dengpao.team/{page_name}">
    <meta property="og:site_name" content="诸葛邓炮">
    
    <!-- Twitter Card Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{final_title}">
    <meta name="twitter:description" content="{final_desc}">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="https://dengpao.team/{page_name}">
'''

def add_seo_to_html(file_path):
    """Add SEO tags to an HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if SEO tags already exist
        if '<meta name="description"' in content:
            print(f"  ⚠️  {file_path} - SEO tags already exist, skipping")
            return False
        
        # Get page name from file path
        page_name = os.path.basename(file_path)
        page_key = page_name.replace('.html', '')
        
        # Generate SEO tags
        seo_tags = generate_seo_tags(page_key)
        
        # Find the closing </title> tag and insert after it
        title_pattern = r'(</title>)'
        
        if re.search(title_pattern, content):
            new_content = re.sub(title_pattern, r'\1\n' + seo_tags.strip(), content, count=1)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"  ✅ {file_path} - SEO tags added")
            return True
        else:
            print(f"  ⚠️  {file_path} - No </title> tag found")
            return False
            
    except Exception as e:
        print(f"  ❌ {file_path} - Error: {e}")
        return False

def main():
    """Main function to optimize all HTML files"""
    workspace = '/Users/bjd/Desktop/ZhugeDengpao-Team'
    
    # Get all HTML files
    html_files = [f for f in os.listdir(workspace) if f.endswith('.html')]
    
    print(f"🔍 Found {len(html_files)} HTML files to optimize\n")
    
    success_count = 0
    for html_file in html_files:
        file_path = os.path.join(workspace, html_file)
        if add_seo_to_html(file_path):
            success_count += 1
    
    print(f"\n✨ Optimization complete!")
    print(f"   Successfully optimized: {success_count}/{len(html_files)} files")

if __name__ == '__main__':
    main()