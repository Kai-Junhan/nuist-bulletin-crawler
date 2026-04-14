import requests
from bs4 import BeautifulSoup
import time
import random

def get_headers(referer_url='https://www.douban.com/'):
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.224 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': referer_url
    }

films = range(0, 250, 25)
No = 1

with open("content.txt", "w", encoding="utf-8") as f:
    f.write("Top 250 电影列表\n")
    f.flush()

    for start_num in films:
        print(f"正在获取第 {start_num//25 + 1} 页...")
        time.sleep(random.uniform(2, 4))
        
        current_url = f"https://movie.douban.com/top250?start={start_num}&filter="
        headers = get_headers(current_url)
        
        response = requests.get(current_url, headers=headers)
        
        print(f"请求状态码: {response.status_code}")
        
        if response.ok:
            soup = BeautifulSoup(response.text, "html.parser")
            
            if soup.title and '豆瓣电影 Top 250' in soup.title.text.strip():
                all_titles = soup.find_all("span", attrs={"class": "title"})
                count_on_page = 0
                
                for title in all_titles:
                    movie_title = title.text.strip()
                    if movie_title and not movie_title.startswith("/"):
                        f.write(f"No.{No} {movie_title}\n")
                        No += 1
                        count_on_page += 1
                
                f.flush()
                print(f"成功获取第 {start_num//25 + 1} 页，本页 {count_on_page} 部，共 {No-1} 部电影")
            else:
                print(f"页面不正确：{soup.title.text.strip() if soup.title else '无标题'}")
                print("可能被反爬，尝试增加延迟")
                time.sleep(10)
        else:
            print("请求失败，状态码：", response.status_code)
            time.sleep(10)
    