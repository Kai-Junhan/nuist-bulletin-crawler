# 南京信息工程大学信息公告栏爬虫

## 项目介绍

本项目用于爬取南京信息工程大学信息公告栏（https://bulletin.nuist.edu.cn/）的内容，仅保存近15天的信息公告。

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
├── README.md           # 项目说明
└── data/                # 数据存储目录
    ├── announcements/   # 公告文件
    └── summary.md       # 内容摘要
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

```bash
python main.py
```

## 功能特点

- 自动爬取公告列表和详情
- 仅保存近15天的公告
- 支持多种HTML结构解析
- 完善的错误处理和重试机制
- Markdown格式存储，便于阅读
- 自动生成内容摘要

## 配置说明

在 `config.py` 中可以修改：
- `DAYS_TO_KEEP`: 保留天数，默认15天
- `REQUEST_DELAY`: 请求延迟范围（秒）
- `REQUEST_RETRIES`: 重试次数

## 注意事项

- 请遵守网站robots.txt规则
- 请勿频繁请求，避免对服务器造成压力
- 本项目仅用于学习目的
