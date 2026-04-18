from tqdm import tqdm
from config import LIST_URL
from requester import get_page
from parser import parse_announcement_list, parse_announcement_detail
from storage import save_announcement, generate_summary
from utils import logger


def main():
    logger.info("=" * 60)
    logger.info("信息公告栏爬虫启动")
    logger.info("=" * 60)
    
    logger.info(f"正在获取公告列表: {LIST_URL}")
    list_response = get_page(LIST_URL, quiet=True)
    
    if not list_response:
        logger.error("\n错误: 无法获取公告列表，程序退出")
        return
    
    announcements = parse_announcement_list(list_response.text, quiet=True)
    
    if not announcements:
        logger.warning("\n警告: 未找到符合条件的公告")
        return
    
    logger.info(f"\n共找到 {len(announcements)} 条近期公告")
    logger.info("\n开始爬取公告详情...")
    logger.info("-" * 60)
    
    saved_files = []
    pbar = tqdm(
        announcements,
        desc="爬取进度",
        unit="条",
        ncols=80,
        bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
        leave=True
    )
    
    for ann in pbar:
        short_title = ann['title'][:20] + "..." if len(ann['title']) > 20 else ann['title']
        pbar.set_postfix_str(f"当前: {short_title}", refresh=False)
        
        detail_response = get_page(ann['link'], quiet=True)
        
        if detail_response:
            detail = parse_announcement_detail(detail_response.text, ann['link'])
            
            if detail.get('publish_date'):
                ann['date'] = detail['publish_date']
            
            filepath = save_announcement(ann, detail, quiet=True)
            if filepath:
                saved_files.append(ann)
    
    pbar.close()
    logger.info("-" * 60)
    
    if saved_files:
        logger.info(f"\n成功保存 {len(saved_files)} 条公告")
        generate_summary(saved_files, quiet=True)
    else:
        logger.warning("\n警告: 未保存任何公告")
    
    logger.info("\n" + "=" * 60)
    logger.info("  爬虫执行完成")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
