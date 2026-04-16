import os

BASE_URL = "https://bulletin.nuist.edu.cn"
LIST_URL = BASE_URL

DAYS_TO_KEEP = 15

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

REQUEST_TIMEOUT = 30
REQUEST_RETRIES = 3
REQUEST_DELAY = (2, 4)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
ANNOUNCEMENTS_DIR = os.path.join(DATA_DIR, 'announcements')
SUMMARY_FILE = os.path.join(DATA_DIR, 'summary.md')

os.makedirs(ANNOUNCEMENTS_DIR, exist_ok=True)
