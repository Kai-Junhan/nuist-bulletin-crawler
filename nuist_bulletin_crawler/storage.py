import os
from datetime import datetime
from utils import logger, sanitize_filename, ensure_dir
from config import ANNOUNCEMENTS_DIR, SUMMARY_FILE


def save_announcement(announcement, detail):
    try:
        final_date = detail.get('publish_date', '')
        
        if not final_date:
            final_date = announcement['date']
        
        if not final_date:
            from datetime import datetime
            final_date = datetime.now().strftime('%Y-%m-%d')
        
        date_str = final_date.replace('/', '-')
        safe_title = sanitize_filename(announcement['title'])
        
        safe_title = safe_title.replace('“', '').replace('”', '').replace('"', '')
        safe_title = safe_title.replace('（', '(').replace('）', ')')
        
        filename = f"{date_str}_{safe_title}.md"
        
        counter = 1
        base_filename = filename
        filepath = os.path.join(ANNOUNCEMENTS_DIR, filename)
        
        while os.path.exists(filepath):
            name, ext = os.path.splitext(base_filename)
            filename = f"{name}_{counter}{ext}"
            filepath = os.path.join(ANNOUNCEMENTS_DIR, filename)
            counter += 1
        
        content = f"# {announcement['title']}\n\n"
        content += f"**发布时间**: {final_date}\n\n"
        content += f"**原始链接**: {announcement['link']}\n\n"
        
        if detail['content']:
            content += "## 正文内容\n\n"
            content += detail['content'] + "\n\n"
        
        if detail['attachments']:
            content += "## 附件\n\n"
            for idx, att in enumerate(detail['attachments'], 1):
                content += f"{idx}. [{att['name']}]({att['url']})\n"
        
        with open(filepath, 'w', encoding='utf-8-sig') as f:
            f.write(content)
        
        logger.info(f"保存公告: {filename}")
        return filepath
        
    except Exception as e:
        logger.error(f"保存公告失败: {e}")
        return None


def generate_summary(announcements):
    try:
        content = f"# 南京信息工程大学信息公告摘要\n\n"
        content += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        content += f"共收录 {len(announcements)} 条公告\n\n"
        content += "---\n\n"
        
        for idx, ann in enumerate(announcements, 1):
            content += f"## {idx}. {ann['title']}\n\n"
            content += f"- 发布时间: {ann['date']}\n"
            content += f"- 链接: {ann['link']}\n\n"
        
        with open(SUMMARY_FILE, 'w', encoding='utf-8-sig') as f:
            f.write(content)
        
        logger.info(f"生成摘要: {SUMMARY_FILE}")
        
    except Exception as e:
        logger.error(f"生成摘要失败: {e}")
