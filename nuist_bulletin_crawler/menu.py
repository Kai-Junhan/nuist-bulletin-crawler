import os
import sys
import ast
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from config import (
    BASE_URL, LIST_URL, DAYS_TO_KEEP,
    REQUEST_TIMEOUT, REQUEST_RETRIES, REQUEST_DELAY
)


def clear_screen():
    """清除屏幕"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """打印标题栏"""
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)


def get_valid_input(prompt, valid_options, default=None):
    """获取有效的用户输入"""
    while True:
        try:
            user_input = input(prompt).strip()
            
            if not user_input and default is not None:
                return default
            
            if user_input in valid_options:
                return user_input
            
            print(f"无效输入！请输入: {', '.join(valid_options)}")
        except KeyboardInterrupt:
            print("\n\n操作被中断")
            return None
        except Exception as e:
            print(f"输入错误: {e}")


def get_number_input(prompt, min_val=None, max_val=None, default=None):
    """获取数字输入"""
    while True:
        try:
            user_input = input(prompt).strip()
            
            if not user_input and default is not None:
                return default
            
            num = int(user_input)
            
            if min_val is not None and num < min_val:
                print(f"输入不能小于 {min_val}")
                continue
            
            if max_val is not None and num > max_val:
                print(f"输入不能大于 {max_val}")
                continue
            
            return num
        except ValueError:
            print("请输入有效的数字！")
        except KeyboardInterrupt:
            print("\n\n操作被中断")
            return None


def config_menu():
    """配置设置菜单"""
    clear_screen()
    print_header("配置设置模块")
    
    config_file = os.path.join(SCRIPT_DIR, 'config.py')
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config_content = f.read()
    
    while True:
        print("\n当前配置:")
        print("-" * 60)
        print(f"1. BASE_URL: {BASE_URL}")
        print(f"2. LIST_URL: {LIST_URL}")
        print(f"3. DAYS_TO_KEEP: {DAYS_TO_KEEP}")
        print(f"4. REQUEST_TIMEOUT: {REQUEST_TIMEOUT}")
        print(f"5. REQUEST_RETRIES: {REQUEST_RETRIES}")
        print(f"6. REQUEST_DELAY: {REQUEST_DELAY}")
        print("-" * 60)
        print("0. 返回主菜单")
        print("-" * 60)
        
        choice = get_valid_input(
            "\n请选择要修改的配置项 (0-6): ",
            ['0', '1', '2', '3', '4', '5', '6']
        )
        
        if choice is None or choice == '0':
            return
        
        if choice == '1':
            new_value = input(f"请输入新的 BASE_URL (当前: {BASE_URL}): ").strip()
            if new_value:
                config_content = config_content.replace(f'BASE_URL = "{BASE_URL}"', f'BASE_URL = "{new_value}"')
        
        elif choice == '2':
            new_value = input(f"请输入新的 LIST_URL (当前: {LIST_URL}): ").strip()
            if new_value:
                config_content = config_content.replace(f'LIST_URL = "{LIST_URL}"', f'LIST_URL = "{new_value}"')
        
        elif choice == '3':
            new_value = get_number_input(
                f"请输入新的 DAYS_TO_KEEP (当前: {DAYS_TO_KEEP}, 范围1-365): ",
                min_val=1, max_val=365, default=DAYS_TO_KEEP
            )
            if new_value is not None:
                config_content = config_content.replace(
                    f'DAYS_TO_KEEP = {DAYS_TO_KEEP}',
                    f'DAYS_TO_KEEP = {new_value}'
                )
        
        elif choice == '4':
            new_value = get_number_input(
                f"请输入新的 REQUEST_TIMEOUT (当前: {REQUEST_TIMEOUT}, 范围5-300): ",
                min_val=5, max_val=300, default=REQUEST_TIMEOUT
            )
            if new_value is not None:
                config_content = config_content.replace(
                    f'REQUEST_TIMEOUT = {REQUEST_TIMEOUT}',
                    f'REQUEST_TIMEOUT = {new_value}'
                )
        
        elif choice == '5':
            new_value = get_number_input(
                f"请输入新的 REQUEST_RETRIES (当前: {REQUEST_RETRIES}, 范围1-10): ",
                min_val=1, max_val=10, default=REQUEST_RETRIES
            )
            if new_value is not None:
                config_content = config_content.replace(
                    f'REQUEST_RETRIES = {REQUEST_RETRIES}',
                    f'REQUEST_RETRIES = {new_value}'
                )
        
        elif choice == '6':
            print(f"当前 REQUEST_DELAY: {REQUEST_DELAY}")
            min_delay = get_number_input(
                "请输入最小延迟 (秒): ",
                min_val=0, default=REQUEST_DELAY[0]
            )
            if min_delay is not None:
                max_delay = get_number_input(
                    "请输入最大延迟 (秒, 必须大于最小延迟): ",
                    min_val=min_delay, default=REQUEST_DELAY[1]
                )
                if max_delay is not None:
                    config_content = config_content.replace(
                        f'REQUEST_DELAY = {REQUEST_DELAY}',
                        f'REQUEST_DELAY = ({min_delay}, {max_delay})'
                    )
        
        confirm = get_valid_input(
            "\n是否保存修改? (yes/no): ",
            ['yes', 'y', 'no', 'n'],
            default='yes'
        )
        
        if confirm in ['yes', 'y']:
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(config_content)
            print("配置已保存！请重新启动菜单以应用更改。")
            return
        else:
            print("修改已取消。")


def run_crawler():
    """运行爬虫"""
    clear_screen()
    print_header("数据爬取操作")
    print("\n正在启动数据爬取...")
    print("-" * 60)
    
    try:
        main_script = os.path.join(SCRIPT_DIR, 'main.py')
        result = subprocess.run(
            [sys.executable, main_script],
            cwd=SCRIPT_DIR
        )
        
        print("\n" + "=" * 60)
        if result.returncode == 0:
            print("爬取操作完成！")
        else:
            print(f"爬取操作返回码: {result.returncode}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n错误: 运行爬虫失败 - {e}")
    
    input("\n按回车键返回主菜单...")


def run_clean_data():
    """运行数据清理"""
    clear_screen()
    print_header("文件删除功能")
    print("\n正在启动数据清理工具...")
    print("-" * 60)
    
    try:
        clean_script = os.path.join(SCRIPT_DIR, 'clean_data.py')
        subprocess.run(
            [sys.executable, clean_script],
            cwd=SCRIPT_DIR
        )
        
    except Exception as e:
        print(f"\n错误: 运行清理工具失败 - {e}")
        input("\n按回车键返回主菜单...")


def main_menu():
    """主菜单"""
    while True:
        clear_screen()
        print_header("信息公告栏 - 功能整合菜单")
        
        print("\n请选择功能:")
        print("-" * 60)
        print("  1. 配置设置 (config)")
        print("  2. 启动数据爬取 (main)")
        print("  3. 执行文件删除 (clean-data)")
        print("-" * 60)
        print("  0. 退出系统")
        print("-" * 60)
        
        choice = get_valid_input(
            "\n请输入选项 (0-3): ",
            ['0', '1', '2', '3']
        )
        
        if choice is None:
            continue
        
        if choice == '0':
            clear_screen()
            print("=" * 60)
            print("谢谢使用,Byebye")
            print("=" * 60)
            break
        
        elif choice == '1':
            config_menu()
        
        elif choice == '2':
            run_crawler()
        
        elif choice == '3':
            run_clean_data()


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        clear_screen()
        print("\n" + "=" * 60)
        print("系统已安全退出")
        print("=" * 60)
    except Exception as e:
        print(f"\n系统错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
