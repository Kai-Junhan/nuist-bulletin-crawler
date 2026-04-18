from config import BASE_URL, LIST_URL
from requester import get_page
from parser import parse_announcement_list
from bs4 import BeautifulSoup


def analyze_structure():
    result = []
    
    result.append("=" * 80)
    result.append("南京信息工程大学公告网页结构分析报告")
    result.append("=" * 80)
    result.append(f"生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    result.append(f"目标网站: {BASE_URL}")
    result.append("")
    
    print("步骤1: 获取公告列表...")
    list_response = get_page(LIST_URL, quiet=True)
    if not list_response:
        print("错误: 无法获取公告列表")
        return
    
    result.append("【1. 公告列表页分析】")
    result.append("-" * 80)
    
    list_soup = BeautifulSoup(list_response.text, 'html.parser')
    
    result.append("\n列表页主要结构:")
    for tag in ['nav', 'ul', 'li', 'div', 'span']:
        tags = list_soup.find_all(tag)
        if tags:
            result.append(f"  - {tag} 标签: {len(tags)} 个")
    
    result.append("\n查找可能的分类导航...")
    nav_elements = list_soup.find_all(['nav', 'div', 'ul'], class_=lambda x: x and any(keyword in x.lower() for keyword in ['nav', 'menu', 'category', 'class', 'type']))
    for i, elem in enumerate(nav_elements[:5]):
        result.append(f"\n  导航元素 {i+1}:")
        result.append(f"    标签: {elem.name}")
        result.append(f"    类名: {elem.get('class', [])}")
        result.append(f"    文本片段: {elem.get_text(strip=True)[:100]}...")
    
    result.append("\n\n【2. 公告详情页分析】")
    result.append("-" * 80)
    
    print("步骤2: 获取公告列表并选择几个详情页...")
    announcements = parse_announcement_list(list_response.text, quiet=True)
    
    if not announcements:
        print("未找到公告")
        return
    
    result.append(f"\n从公告列表中选择 {min(5, len(announcements))} 个公告进行详细分析:")
    
    sample_urls = [ann['link'] for ann in announcements[:5]]
    
    category_words = set()
    possible_locations = set()
    
    for idx, url in enumerate(sample_urls):
        result.append(f"\n{'='*80}")
        result.append(f"公告 {idx+1}: {url}")
        result.append(f"{'='*80}")
        
        print(f"\n正在分析第 {idx+1} 个公告: {url}")
        detail_response = get_page(url, quiet=True)
        
        if not detail_response:
            result.append("  无法获取此页面")
            continue
        
        soup = BeautifulSoup(detail_response.text, 'html.parser')
        
        result.append("\n  [HTML 结构概览]")
        result.append(f"  标题: {soup.title.get_text(strip=True) if soup.title else '无'}")
        
        result.append("\n  [查找面包屑导航]")
        breadcrumbs = soup.find_all(['div', 'ul', 'ol'], class_=lambda x: x and any(k in x.lower() for k in ['bread', 'crumb', 'location', 'nav', 'path']))
        if breadcrumbs:
            for i, bc in enumerate(breadcrumbs[:3]):
                text = bc.get_text(' ', strip=True)
                result.append(f"  面包屑 {i+1}: {text}")
                possible_locations.add("面包屑导航")
                words = text.split()
                for word in words:
                    if len(word) >= 2 and '公告' not in word and '首页' not in word:
                        category_words.add(word)
        else:
            result.append("  未找到标准面包屑导航，尝试其他可能位置...")
        
        result.append("\n  [查找文章元数据区域]")
        metadata_divs = soup.find_all(['div', 'p', 'span'], class_=lambda x: x and any(k in x.lower() for k in ['arti', 'article', 'meta', 'info', 'publish']))
        for i, md in enumerate(metadata_divs[:5]):
            text = md.get_text(strip=True)
            if text:
                result.append(f"  元数据区域 {i+1}: {text}")
                possible_locations.add("文章元数据区域")
                if '分类' in text or '栏目' in text or '类型' in text:
                    category_words.add(text.split('：')[-1] if '：' in text else text)
        
        result.append("\n  [查找所有链接文本]")
        all_links = soup.find_all('a', href=True)
        link_texts = [a.get_text(strip=True) for a in all_links if len(a.get_text(strip=True)) >= 2]
        result.append(f"  前20个链接文本: {', '.join(link_texts[:20])}")
        for lt in link_texts:
            if len(lt) <= 10 and '公告' not in lt and '首页' not in lt and '下载' not in lt:
                category_words.add(lt)
        
        result.append("\n  [查找标题上方/周围的文本]")
        h1_tag = soup.find('h1')
        if h1_tag:
            prev_siblings = []
            for sibling in h1_tag.previous_siblings:
                if hasattr(sibling, 'get_text'):
                    text = sibling.get_text(strip=True)
                    if text and len(text) < 50:
                        prev_siblings.append(text)
            result.append(f"  标题上方文本: {', '.join(reversed(prev_siblings))}")
            for text in prev_siblings:
                category_words.add(text)
        
        result.append("\n  [保存原始HTML片段用于参考]")
        with open(f'page_{idx+1}_sample.html', 'w', encoding='utf-8') as f:
            f.write(detail_response.text[:10000])
        result.append(f"  HTML片段已保存到 page_{idx+1}_sample.html")
    
    result.append("\n\n")
    result.append("=" * 80)
    result.append("【3. 分析总结】")
    result.append("=" * 80)
    
    result.append("\n分类词可能的位置:")
    for loc in possible_locations:
        result.append(f"  - {loc}")
    
    result.append("\n发现的分类词示例:")
    for word in sorted(category_words):
        if len(word) >= 2 and len(word) <= 15:
            result.append(f"  - {word}")
    
    result.append("\n\n")
    result.append("=" * 80)
    result.append("分析完成！")
    result.append("=" * 80)
    
    final_text = '\n'.join(result)
    print("\n\n" + final_text)
    
    with open('analysis_result.txt', 'w', encoding='utf-8') as f:
        f.write(final_text)
    
    print(f"\n结果已保存到 analysis_result.txt")


if __name__ == "__main__":
    analyze_structure()
