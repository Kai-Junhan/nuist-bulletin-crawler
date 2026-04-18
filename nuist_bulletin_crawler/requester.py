import time
import random
import requests
from utils import logger
from config import REQUEST_HEADERS, REQUEST_TIMEOUT, REQUEST_RETRIES, REQUEST_DELAY


def get_page(url, retries=REQUEST_RETRIES, quiet=False):
    for attempt in range(retries):
        try:
            delay = random.uniform(*REQUEST_DELAY)
            time.sleep(delay)
            
            response = requests.get(
                url,
                headers=REQUEST_HEADERS,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            response.encoding = 'utf-8'
            
            if not quiet:
                logger.info(f"成功获取页面: {url}")
            return response
            
        except requests.exceptions.ConnectionError as e:
            logger.warning(f"连接错误 (尝试 {attempt + 1}/{retries}): {e}")
        except requests.exceptions.Timeout as e:
            logger.warning(f"请求超时 (尝试 {attempt + 1}/{retries}): {e}")
        except requests.exceptions.RequestException as e:
            logger.warning(f"请求异常 (尝试 {attempt + 1}/{retries}): {e}")
        
        if attempt < retries - 1:
            time.sleep(5)
    
    logger.error(f"无法获取页面，已重试 {retries} 次: {url}")
    return None
