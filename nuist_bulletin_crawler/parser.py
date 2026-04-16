from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import re
from utils import logger, is_within_days
from config import BASE_URL


def extract_date(text):
    date_patterns = [
        r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})',
        r'(\d{4})年(\d{1,2})月(\d{1,2})日',
        r'发布时间[：:]\s*(\d{4})[-/](\d{1,2})[-/](\d{1,2})'
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            if len(match.groups()) == 3:
                year, month, day = match.groups()
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    
    return ''


def parse_announcement_list(html):
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    announcements = []
    
    logger.info("开始解析公告列表...")
    
    all_links = soup.find_all('a', href=True)
    logger.info(f"找到 {len(all_links)} 个链接")
    
    content_links = []
    for a in all_links:
        href = a.get('href', '')
        if 'content.jsp' in href:
            content_links.append(a)
    
    logger.info(f"找到 {len(content_links)} 个 content.jsp 链接")
    
    for a in content_links:
        try:
            title = a.get_text(strip=True)
            if not title or len(title) < 5:
                continue
            
            link = a['href']
            if link and not link.startswith('http'):
                link = urljoin(BASE_URL, link)
            
            parent_text = a.parent.get_text() if a.parent else ''
            pub_date = extract_date(parent_text)
            
            if not pub_date:
                pub_date = extract_date(a.get_text())
            
            if not pub_date:
                pub_date = datetime.now().strftime('%Y-%m-%d')
            
            if is_within_days(pub_date):
                announcements.append({
                    'title': title,
                    'link': link,
                    'date': pub_date
                })
                logger.info(f"找到公告: {title} ({pub_date})")
            
            if len(announcements) >= 50:
                break
                
        except Exception as e:
            logger.debug(f"解析公告项失败: {e}")
    
    if not announcements:
        logger.warning("未找到符合条件的公告，尝试使用全部链接...")
        for a in content_links[:10]:
            title = a.get_text(strip=True)
            if len(title) > 5:
                link = a['href']
                if link and not link.startswith('http'):
                    link = urljoin(BASE_URL, link)
                announcements.append({
                    'title': title,
                    'link': link,
                    'date': datetime.now().strftime('%Y-%m-%d')
                })
                logger.info(f"找到链接: {title}")
    
    logger.info(f"共找到 {len(announcements)} 条公告")
    return announcements


def parse_announcement_detail(html, url):
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    
    result = {
        'title': '',
        'content': '',
        'attachments': []
    }
    
    try:
        title_tag = soup.find('h1')
        if title_tag:
            result['title'] = title_tag.get_text(strip=True)
        else:
            title_tag = soup.find('title')
            if title_tag:
                result['title'] = title_tag.get_text(strip=True).replace('-信息公告栏', '').strip()
        
        content_tag = soup.find('div', class_='article')
        if content_tag:
            seen = set()
            content_parts = []
            paragraphs = content_tag.find_all(['p', 'div'])
            for p in paragraphs:
                text = p.get_text('\n', strip=True)
                if text and text not in seen:
                    seen.add(text)
                    content_parts.append(text)
            result['content'] = '\n\n'.join(content_parts)
        
        if not result['content']:
            body_tag = soup.find('body')
            if body_tag:
                result['content'] = body_tag.get_text('\n', strip=True)
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            text = a_tag.get_text(strip=True)
            
            if any(ext in href.lower() for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip', '.rar']):
                if not href.startswith('http'):
                    href = urljoin(BASE_URL, href)
                result['attachments'].append({
                    'name': text or href.split('/')[-1],
                    'url': href
                })
    
    except Exception as e:
        logger.error(f"解析公告详情失败: {e}")
    
    return result
