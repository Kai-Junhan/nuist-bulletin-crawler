from tqdm import tqdm
from config import LIST_URL
from requester import get_page
from parser import parse_announcement_list, parse_announcement_detail
from storage import save_announcement, generate_summary
from utils import logger


def main():
    logger.info("=" * 50)
    logger.info("南京信息工程大学信息公告栏爬虫启动")
    logger.info("=" * 50)
    
    logger.info(f"正在获取公告列表: {LIST_URL}")
    list_response = get_page(LIST_URL)
    
    if not list_response:
        logger.error("无法获取公告列表，程序退出")
        return
    
    announcements = parse_announcement_list(list_response.text)
    
    if not announcements:
        logger.warning("未找到符合条件的公告")
        return
    
    logger.info(f"共找到 {len(announcements)} 条近期公告")
    
    saved_files = []
    for ann in tqdm(announcements, desc="爬取公告详情"):
        logger.info(f"正在获取: {ann['title']}")
        detail_response = get_page(ann['link'])
        
        if detail_response:
            detail = parse_announcement_detail(detail_response.text, ann['link'])
            filepath = save_announcement(ann, detail)
            if filepath:
                saved_files.append(ann)
    
    if saved_files:
        logger.info(f"成功保存 {len(saved_files)} 条公告")
        generate_summary(saved_files)
    else:
        logger.warning("未保存任何公告")
    
    logger.info("=" * 50)
    logger.info("爬虫执行完成")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
