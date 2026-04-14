import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54"}

response = requests.get("https://www.book.toscrape.com",headers)
print(response)
if response.ok:
    print(response.text)
else:
    print("请求失败，状态码：", response.status_code)
    