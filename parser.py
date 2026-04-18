from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import re
from utils import logger, is_within_days
from config import BASE_URL


def extract_category(html, is_detail=False):
    soup = BeautifulSoup(html, 'html.parser')
    
    if is_detail:
        keywords_meta = soup.find('meta', {'name': 'keywords'})
        if keywords_meta:
            content = keywords_meta.get('content', '')
            keywords = [k.strip() for k in content.split(',') if k.strip()]
            if len(keywords) >= 2:
                return keywords[1]
    else:
        wjj_span = soup.find('span', class_='wjj')
        if wjj_span:
            text = wjj_span.get_text(strip=True)
            return text.strip('[]')
    
    return '其他'


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


def parse_announcement_list(html, quiet=False):
    soup = BeautifulSoup(html, 'html.parser')
    announcements = []
    
    if not quiet:
        logger.info("开始解析公告列表...")
    
    news_items = soup.find_all('li', class_='news')
    if not quiet:
        logger.info(f"找到 {len(news_items)} 个公告项")
    
    for item in news_items:
        try:
            a_tag = item.find('a', href=True)
            if not a_tag:
                continue
                
            href = a_tag.get('href', '')
            if 'content.jsp' not in href and 'info/' not in href:
                continue
            
            title = a_tag.get_text(strip=True)
            if not title or len(title) < 5:
                continue
            
            link = href
            if link and not link.startswith('http'):
                link = urljoin(BASE_URL, link)
            
            category = '其他'
            wjj_span = item.find('span', class_='wjj')
            if wjj_span:
                category_text = wjj_span.get_text(strip=True)
                category = category_text.strip('[]')
            
            pub_date = ''
            date_span = item.find('span', class_='arti_bs')
            if date_span:
                pub_date = date_span.get_text(strip=True)
            
            if not pub_date:
                parent_text = item.get_text()
                pub_date = extract_date(parent_text)
            
            if not pub_date:
                pub_date = ''
            
            if is_within_days(pub_date):
                announcements.append({
                    'title': title,
                    'link': link,
                    'date': pub_date,
                    'category': category
                })
                if not quiet:
                    logger.info(f"找到公告: {title} ({pub_date})")
            
            if len(announcements) >= 50:
                break
                
        except Exception as e:
            logger.debug(f"解析公告项失败: {e}")
    
    if not announcements:
        logger.warning("未找到符合条件的公告，尝试使用全部链接...")
        all_links = soup.find_all('a', href=True)
        content_links = []
        for a in all_links:
            href = a.get('href', '')
            if 'content.jsp' in href or 'info/' in href:
                content_links.append(a)
        
        for a in content_links[:10]:
            title = a.get_text(strip=True)
            if len(title) > 5:
                link = a['href']
                if link and not link.startswith('http'):
                    link = urljoin(BASE_URL, link)
                
                category = '其他'
                wjj_span = a.find_parent('li', class_='news')
                if wjj_span:
                    wjj = wjj_span.find('span', class_='wjj')
                    if wjj:
                        category_text = wjj.get_text(strip=True)
                        category = category_text.strip('[]')
                
                announcements.append({
                    'title': title,
                    'link': link,
                    'date': '',
                    'category': category
                })
                if not quiet:
                    logger.info(f"找到链接: {title}")
    
    if not quiet:
        logger.info(f"共找到 {len(announcements)} 条公告")
    return announcements


def parse_announcement_detail(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    
    result = {
        'title': '',
        'content': '',
        'attachments': [],
        'publish_date': '',
        'category': ''
    }
    
    category = '其他'
    keywords_meta = soup.find('meta', {'name': 'keywords'})
    if keywords_meta:
        content = keywords_meta.get('content', '')
        keywords = [k.strip() for k in content.split(',') if k.strip()]
        if len(keywords) >= 2:
            category = keywords[1]
    result['category'] = category
    
    try:
        date_tag = soup.find('span', class_='arti_update')
        if date_tag:
            date_text = date_tag.get_text(strip=True)
            result['publish_date'] = extract_date(date_text)
        
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
