import os
import re
import logging
from datetime import datetime, timedelta
from config import DAYS_TO_KEEP

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def sanitize_filename(filename):
    invalid_chars = r'[<>:"/\\|?*]'
    filename = re.sub(invalid_chars, '_', filename)
    filename = filename.strip()
    filename = filename[:80]
    
    try:
        filename.encode('gbk')
    except UnicodeEncodeError:
        filename = filename.encode('utf-8', errors='ignore').decode('utf-8')
    
    return filename


def is_within_days(date_str, days=DAYS_TO_KEEP):
    try:
        if '-' in date_str:
            pub_date = datetime.strptime(date_str, '%Y-%m-%d')
        elif '/' in date_str:
            pub_date = datetime.strptime(date_str, '%Y/%m/%d')
        else:
            return False
        
        cutoff_date = datetime.now() - timedelta(days=days)
        return pub_date >= cutoff_date
    except Exception as e:
        logger.error(f"日期解析错误: {e}")
        return False


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"创建目录: {directory}")


def format_datetime(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')
