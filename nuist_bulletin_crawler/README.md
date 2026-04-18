# 南京信息工程大学信息公告栏爬虫

## 项目介绍

本项目用于爬取南京信息工程大学信息公告栏（https://bulletin.nuist.edu.cn/）的内容，仅保存近15天的信息公告。

## 数据存储说明

- **数据行为**：data目录中的数据是累加的，不会自动覆盖
- 公告文件会按日期和标题保存到 `data/announcements/` 目录
- 如果有相同文件名会自动添加序号（如 `_1`, `_2`）
- `summary.md` 文件会被覆盖，但公告文件会保留

## 文件夹结构

```
nuist_bulletin_crawler/
├── main.py              # 主程序入口
├── clean_data.py         # 数据清理脚本
├── config.py            # 配置文件
├── requester.py         # 网页请求模块
├── parser.py            # 数据解析模块
├── storage.py           # 结果存储模块
├── utils.py             # 工具函数模块
├── requirements.txt     # 依赖列表
├── README.md           # 项目说明
├── TIME_FIX.md         # 时间修复记录
└── data/                # 数据存储目录
    ├── announcements/   # 公告文件
    └── summary.md       # 内容摘要
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 运行爬虫

```bash
python main.py
```

### 清理数据

如需清除data目录中的所有文件（保留目录结构），运行：

```bash
python clean_data.py
```

数据清理脚本功能：
1. 扫描data目录及其所有子目录
2. 显示即将删除的文件数量及路径
3. 要求用户确认后再执行删除
4. 删除所有文件但保留目录结构
5. 处理删除错误并继续执行后续操作
6. 生成详细的操作报告（保存为 clean_report.txt）

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
