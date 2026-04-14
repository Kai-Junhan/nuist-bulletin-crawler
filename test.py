# -*- coding: utf-8 -*-
"""
这是一个简单的网页爬虫程序
功能：从指定网址获取页面标题并保存到文件
作者：初学者示例
"""

# 导入需要的库
import requests          # requests库：用于发送HTTP请求，获取网页内容
from bs4 import BeautifulSoup  # BeautifulSoup库：用于解析HTML文档，提取所需信息

# 定义要爬取的网址（这里以百度首页为例）
url = "https://i.nuist.edu.cn/default/index.html#/newList?cardId=CUS_CARD_NEWSNUIST&cardWid=781119293634152&channelIds=1371622295452393473"

# 使用requests库的get方法向网址发送HTTP GET请求
# 这会模拟浏览器访问网页，获取网页的源代码
res = requests.get(url)

# 【关键修复】手动设置正确的编码
# 网页可能使用不同的编码方式（如GBK、UTF-8等）
# 如果不设置正确的编码，中文可能会显示为乱码
# UTF-8是最常用的编码格式，支持中文等多语言字符
res.encoding = 'utf-8'

# 创建BeautifulSoup对象来解析网页内容
# 参数1：res.text - 网页的文本内容
# 参数2："html.parser" - 使用Python内置的HTML解析器
# soup对象就像一个树形结构，可以方便地查找和提取HTML中的元素
soup = BeautifulSoup(res.text, "html.parser")

# 从解析后的网页中查找<title>标签，并获取其中的文本内容
# find("title") - 查找第一个<title>标签
# .text - 获取标签内的纯文本内容（不包含HTML标记）
title = soup.find("title").text

# 将结果保存到文件中
# open()函数打开（或创建）一个文件
# 参数1："result.txt" - 文件名
# 参数2："w" - 写入模式（如果文件已存在会覆盖，不存在则创建）
# 参数3：encoding="utf-8" - 使用UTF-8编码保存文件，确保中文正常显示
with open("result.txt", "w", encoding="utf-8") as f:
    # 向文件中写入文字说明
    f.write("爬取成功！页面标题：")
    # 向文件中写入获取到的页面标题
    f.write(title)

# 在控制台打印提示信息，告知用户程序执行完成
print("Done! Check result.txt now!")
