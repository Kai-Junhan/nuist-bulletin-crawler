#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试分类词提取功能
"""
import os
from parser import parse_announcement_list, parse_announcement_detail
from storage import save_announcement

def test_parse_list():
    print("=" * 60)
    print("测试列表页解析")
    print("=" * 60)
    
    with open('homepage.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    announcements = parse_announcement_list(html, quiet=False)
    
    print(f"\n找到 {len(announcements)} 条公告")
    print("\n前5条公告:")
    for idx, ann in enumerate(announcements[:5], 1):
        print(f"{idx}. [{ann.get('category', 'N/A')}] {ann['title']}")
    
    return announcements

def test_parse_detail():
    print("\n" + "=" * 60)
    print("测试详情页解析")
    print("=" * 60)
    
    with open('detail_1.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    detail = parse_announcement_detail(html, 'https://bulletin.nuist.edu.cn/detail_1.html')
    
    print(f"\n标题: {detail['title']}")
    print(f"分类: {detail['category']}")
    print(f"发布日期: {detail['publish_date']}")
    
    return detail

def test_save():
    print("\n" + "=" * 60)
    print("测试保存功能")
    print("=" * 60)
    
    with open('detail_1.html', 'r', encoding='utf-8') as f:
        html_detail = f.read()
    
    with open('homepage.html', 'r', encoding='utf-8') as f:
        html_list = f.read()
    
    announcements = parse_announcement_list(html_list, quiet=True)
    if announcements:
        ann = announcements[0]
        detail = parse_announcement_detail(html_detail, ann['link'])
        
        filepath = save_announcement(ann, detail, quiet=False)
        
        if filepath and os.path.exists(filepath):
            print(f"\n文件已保存: {filepath}")
            
            print("\n文件内容预览:")
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                print(f.read(500))
    
if __name__ == '__main__':
    try:
        test_parse_list()
        test_parse_detail()
        test_save()
        print("\n" + "=" * 60)
        print("测试完成！")
        print("=" * 60)
    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()
