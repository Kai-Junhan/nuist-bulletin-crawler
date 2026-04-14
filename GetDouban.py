import requests
from bs4 import BeautifulSoup
import time
import random

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.224 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://www.douban.com/'
}

films = range(0, 250, 25)
No = 1

with open("content.txt", "w", encoding="utf-8") as f:
    f.write("Top 250 电影列表\n")

    for start_num in films:     
        # 随机延迟， 避免被反爬
        time.sleep(random.uniform(1, 3))
        
        response = requests.get(f"https://movie.douban.com/top250?start={start_num}&filter=", headers=headers)
        
        if response.ok:
            soup = BeautifulSoup(response.text, "html.parser")
            # 检查是否是正确的页面
            # 检查页面标题是否存在且包含正确的内容
            if soup.title and '豆瓣电影 Top 250' in soup.title.text:
                all_titles = soup.find_all("span", attrs={"class": "title"})
                for title in all_titles:
                    movie_title = title.text.strip()
                    if movie_title and not movie_title.startswith("/"):
                        f.write(f"No.{No} {movie_title}\n")  
                        No += 1
                        
                headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.224 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                        'Referer': f'https://movie.douban.com/top250?start={start_num}&filter='
                }
                print(f"成功获取第 {start_num//25 + 1} 页，已获取 {No-1} 部电影")
            else:
                print(f"页面不正确：{soup.title.text if soup.title else '无标题'}")
                print("可能被反爬，尝试增加延迟")
                time.sleep(5)
        else:
            print("请求失败，状态码：", response.status_code)
            # 失败时增加延迟
            time.sleep(5)
    