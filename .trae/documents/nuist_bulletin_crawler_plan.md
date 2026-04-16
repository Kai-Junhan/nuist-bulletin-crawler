# 南京信息工程大学信息公告栏爬虫项目计划

## 项目概述
创建一个完整的爬虫项目，用于爬取南京信息工程大学信息公告栏（https://bulletin.nuist.edu.cn/）的内容，仅保存近15天的信息公告。

## 文件夹结构
```
nuist_bulletin_crawler/
├── main.py              # 主程序入口
├── config.py            # 配置文件
├── requester.py         # 网页请求模块
├── parser.py            # 数据解析模块
├── storage.py           # 结果存储模块
├── utils.py             # 工具函数模块
├── requirements.txt     # 依赖列表
└── data/                # 数据存储目录
    ├── announcements/   # 公告文件
    └── summary.md       # 内容摘要
```

## 核心功能模块

### 1. requester.py - 网页请求模块
- 发送HTTP请求获取页面内容
- 添加请求头和超时设置
- 处理连接错误、超时等异常
- 实现重试机制

### 2. parser.py - 数据解析模块
- 解析公告列表页面
- 解析公告详情页面
- 提取标题、发布时间、内容、附件等信息
- 时间过滤（仅保留近15天）

### 3. storage.py - 结果存储模块
- 按日期分类存储公告
- 保存为Markdown格式
- 下载并保存附件文件
- 生成内容摘要

### 4. config.py - 配置文件
- 网站URL配置
- 时间过滤配置
- 请求头配置
- 存储路径配置

### 5. utils.py - 工具函数
- 日期处理函数
- 文件操作函数
- 字符串处理函数
- 日志记录函数

### 6. main.py - 主程序
- 整合所有模块
- 控制爬取流程
- 进度显示
- 错误处理

## 技术要点

### 依赖库
- requests: HTTP请求
- beautifulsoup4: HTML解析
- python-dateutil: 日期处理
- tqdm: 进度条显示

### 时间过滤逻辑
- 获取公告发布时间
- 计算与当前时间的差值
- 仅保存15天内的内容

### 数据存储格式
- 每个公告保存为独立的Markdown文件
- 文件名格式：`YYYY-MM-DD_标题.md`
- 包含：标题、发布时间、来源、正文、附件链接

### 错误处理
- 网络异常处理
- 解析异常处理
- 文件操作异常处理
- 日志记录

## 实现步骤

1. 创建项目文件夹结构
2. 实现config.py配置模块
3. 实现utils.py工具模块
4. 实现requester.py请求模块
5. 实现parser.py解析模块
6. 实现storage.py存储模块
7. 实现main.py主程序
8. 创建requirements.txt
9. 测试和调试

## 注意事项
- 遵守网站robots.txt规则
- 添加适当的延迟，避免对服务器造成压力
- 尊重版权，仅用于学习目的
