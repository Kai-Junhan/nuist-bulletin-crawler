from config import BASE_URL
from requester import get_page
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def simple_analyze():
    result = []
    
    result.append("=" * 80)
    result.append("南京信息工程大学公告网页结构分析报告")
    result.append("=" * 80)
    result.append(f"生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    result.append(f"目标网站: {BASE_URL}")
    result.append("")
    
    print(f"正在获取首页: {BASE_URL}")
    response = get_page(BASE_URL, quiet=True)
    
    if not response:
        print("错误: 无法获取首页")
        return
    
    with open('homepage.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("首页HTML已保存到 homepage.html")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    result.append("\n【首页HTML结构分析】")
    result.append("-" * 80)
    
    # 查找所有 content.jsp 链接
    content_links = []
    all_links = soup.find_all('a', href=True)
    for a in all_links:
        href = a['href']
        if 'content.jsp' in href:
            if not href.startswith('http'):
                href = urljoin(BASE_URL, href)
            content_links.append(href)
    
    content_links = list(set(content_links))[:5]  # 去重并取前5个
    result.append(f"\n找到 {len(content_links)} 个公告详情链接:")
    for i, link in enumerate(content_links):
        result.append(f"  {i+1}. {link}")
    
    # 分析这些详情页
    category_words = set()
    possible_locations = set()
    
    for idx, url in enumerate(content_links):
        result.append(f"\n{'='*80}")
        result.append(f"公告 {idx+1}: {url}")
        result.append(f"{'='*80}")
        
        print(f"\n正在分析第 {idx+1} 个公告...")
        detail_response = get_page(url, quiet=True)
        
        if not detail_response:
            result.append("  无法获取此页面")
            continue
        
        # 保存HTML片段
        with open(f'detail_{idx+1}.html', 'w', encoding='utf-8') as f:
            f.write(detail_response.text)
        result.append(f"  完整HTML已保存到 detail_{idx+1}.html")
        
        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
        
        result.append(f"\n  页面标题: {detail_soup.title.get_text(strip=True) if detail_soup.title else '无'}")
        
        # 查找所有文本内容
        result.append("\n  [查找所有可能包含分类的区域]")
        
        # 1. 查找所有 div 并查看 class 属性
        divs = detail_soup.find_all('div', class_=True)
        result.append(f"\n  找到 {len(divs)} 个带 class 的 div，前 10 个:")
        for i, div in enumerate(divs[:10]):
            class_list = div.get('class', [])
            text = div.get_text(strip=True)[:80]
            result.append(f"    {i+1}. class={class_list}, 内容='{text}...'")
        
        # 2. 查找所有包含 "当前位置"、"分类"、"栏目" 等关键词的文本
        all_text = detail_soup.get_text('\n', strip=True)
        lines = [line for line in all_text.split('\n') if line.strip()]
        result.append(f"\n  包含关键词的行:")
        for line in lines:
            if any(keyword in line for keyword in ['当前', '位置', '分类', '栏目', '类型', '所属']):
                result.append(f"    - {line}")
                possible_locations.add(line)
                
                # 提取可能的分类词
                if '：' in line or ':' in line:
                    parts = line.split('：') if '：' in line else line.split(':')
                    if len(parts) > 1:
                        category = parts[1].strip()
                        if category:
                            category_words.add(category)
        
        # 3. 查找所有导航链接
        nav_links = detail_soup.find_all('a', href=True)
        result.append(f"\n  导航链接文本（前20个）:")
        link_texts = []
        for a in nav_links:
            text = a.get_text(strip=True)
            if text and 2 <= len(text) <= 10:
                link_texts.append(text)
        link_texts = list(set(link_texts))[:20]
        for text in link_texts:
            result.append(f"    - {text}")
            category_words.add(text)
    
    result.append("\n\n")
    result.append("=" * 80)
    result.append("【总结】")
    result.append("=" * 80)
    
    result.append("\n分类词可能的位置/关键词:")
    for loc in possible_locations:
        result.append(f"  - {loc}")
    
    result.append("\n发现的分类词示例:")
    for word in sorted(category_words):
        if 2 <= len(word) <= 15:
            result.append(f"  - {word}")
    
    final_text = '\n'.join(result)
    print("\n\n" + final_text)
    
    with open('analysis_result.txt', 'w', encoding='utf-8') as f:
        f.write(final_text)
    
    print(f"\n结果已保存到 analysis_result.txt")

if __name__ == "__main__":
    simple_analyze()
