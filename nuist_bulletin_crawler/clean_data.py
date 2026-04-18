import os
import sys
from datetime import datetime
from config import DATA_DIR, BASE_DIR


def scan_files(directory):
    """扫描目录并返回所有文件路径"""
    files_to_delete = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            files_to_delete.append(file_path)
    
    return files_to_delete


def confirm_deletion(files):
    """向用户确认删除操作"""
    print("=" * 60)
    print("数据清理工具")
    print("=" * 60)
    print(f"\n目标目录: {DATA_DIR}")
    print(f"找到 {len(files)} 个文件将被删除\n")
    
    if len(files) == 0:
        print("没有找到需要删除的文件。")
        return False
    
    print("即将删除的文件:")
    print("-" * 60)
    
    for i, file_path in enumerate(files[:20], 1):
        rel_path = os.path.relpath(file_path, BASE_DIR)
        print(f"  {i}. {rel_path}")
    
    if len(files) > 20:
        print(f"  ... 还有 {len(files) - 20} 个文件")
    
    print("-" * 60)
    print("\n警告: 此操作将删除上述所有文件！")
    print("目录结构将被保留，仅删除文件。")
    
    while True:
        choice = input("\n确认继续删除吗? (yes/no): ").strip().lower()
        if choice in ['yes', 'y']:
            return True
        elif choice in ['no', 'n']:
            return False
        else:
            print("请输入 'yes' 或 'no'")


def delete_files(files):
    """删除文件并记录结果"""
    success_count = 0
    failed_files = []
    success_files = []
    
    for file_path in files:
        try:
            os.remove(file_path)
            success_count += 1
            success_files.append(file_path)
            print(f"✓ 删除成功: {os.path.relpath(file_path, BASE_DIR)}")
        except Exception as e:
            failed_files.append({
                'path': file_path,
                'error': str(e)
            })
            print(f"✗ 删除失败: {os.path.relpath(file_path, BASE_DIR)} - {e}")
    
    return success_count, success_files, failed_files


def generate_report(success_count, success_files, failed_files, start_time):
    """生成操作报告"""
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    report_path = os.path.join(BASE_DIR, 'clean_report.txt')
    
    report_content = []
    report_content.append("=" * 60)
    report_content.append("数据清理操作报告")
    report_content.append("=" * 60)
    report_content.append(f"\n开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    report_content.append(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    report_content.append(f"执行时长: {duration:.2f} 秒")
    report_content.append(f"\n成功删除: {success_count} 个文件")
    report_content.append(f"删除失败: {len(failed_files)} 个文件")
    
    if success_files:
        report_content.append("\n" + "=" * 60)
        report_content.append("成功删除的文件:")
        report_content.append("=" * 60)
        for file_path in success_files:
            report_content.append(f"  ✓ {os.path.relpath(file_path, BASE_DIR)}")
    
    if failed_files:
        report_content.append("\n" + "=" * 60)
        report_content.append("删除失败的文件:")
        report_content.append("=" * 60)
        for item in failed_files:
            report_content.append(f"  ✗ {os.path.relpath(item['path'], BASE_DIR)}")
            report_content.append(f"    错误: {item['error']}")
    
    report_content.append("\n" + "=" * 60)
    report_content.append("报告结束")
    report_content.append("=" * 60)
    
    report_text = "\n".join(report_content)
    
    with open(report_path, 'w', encoding='utf-8-sig') as f:
        f.write(report_text)
    
    print(f"\n{'='*60}")
    print(f"操作报告已保存到: {os.path.relpath(report_path, BASE_DIR)}")
    print(f"{'='*60}")
    
    return report_path


def main():
    """主函数"""
    start_time = datetime.now()
    
    if not os.path.exists(DATA_DIR):
        print(f"错误: 数据目录不存在: {DATA_DIR}")
        return 1
    
    print("正在扫描文件...")
    files = scan_files(DATA_DIR)
    
    if not confirm_deletion(files):
        print("\n操作已取消。")
        return 0
    
    print("\n开始删除文件...")
    print("-" * 60)
    success_count, success_files, failed_files = delete_files(files)
    print("-" * 60)
    
    generate_report(success_count, success_files, failed_files, start_time)
    
    print(f"\n清理完成!")
    print(f"成功: {success_count} 个文件")
    print(f"失败: {len(failed_files)} 个文件")
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n操作被用户中断。")
        sys.exit(1)
    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
