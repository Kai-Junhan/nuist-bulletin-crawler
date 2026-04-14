import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54"}

films = range(0, 250, 25)
No = 1

for start_num in films:
    response = requests.get(f"https://movie.douban.com/top250?start={start_num}",headers=headers)
    
    if response.ok:
        soup = BeautifulSoup(response.text, "html.parser")
        all_titles = soup.find_all("span", attrs={"class": "title"})
        for title in all_titles:
            movie_title = title.text.strip()
            if movie_title and not movie_title.startswith("/"):
                print("No."+f"{No} {movie_title}")  
                No += 1
    else:
        print("请求失败，状态码：", response.status_code)
    