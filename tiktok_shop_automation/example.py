"""
TikTok店铺自动化使用示例
演示如何在自己的代码中使用自动化类
"""

from main import TikTokShopAutomation
from utils import load_config


def example_basic_usage():
    """基本使用示例"""
    print("=== 基本使用示例 ===")

    # 创建自动化实例
    automation = TikTokShopAutomation()

    # 运行自动化任务
    success = automation.run()

    if success:
        print("✅ 任务执行成功")
    else:
        print("❌ 任务执行失败")


def example_custom_config():
    """使用自定义配置示例"""
    print("=== 自定义配置示例 ===")

    # 使用自定义配置文件
    automation = TikTokShopAutomation(config_path='config/my_config.yaml')
    automation.run()


def example_programmatic_config():
    """程序化配置示例"""
    print("=== 程序化配置示例 ===")

    # 加载配置
    config = load_config()

    # 修改配置
    config['scraping']['max_pages'] = 5  # 只抓取5页
    config['storage']['format'] = 'json'  # 保存为JSON格式

    # 注意：这种方式需要将修改后的配置传递给automation
    # 或者将配置保存到临时文件后再加载


def example_data_processing():
    """数据处理示例"""
    print("=== 数据处理示例 ===")

    import pandas as pd

    # 假设已经运行过自动化任务，数据保存在 data/ 目录
    # 读取最新的Excel文件
    import glob
    import os

    data_files = glob.glob('data/tiktok_popular_products_*.xlsx')
    if data_files:
        latest_file = max(data_files, key=os.path.getctime)
        print(f"读取文件: {latest_file}")

        df = pd.read_excel(latest_file)

        print(f"\n总商品数: {len(df)}")
        print(f"\n前5个商品:")
        print(df.head())

        # 数据分析示例
        if 'price' in df.columns:
            print(f"\n价格统计:")
            print(df['price'].describe())

        if 'sales' in df.columns:
            print(f"\n销量前10的商品:")
            top_sales = df.nlargest(10, 'sales')
            print(top_sales[['product_name', 'sales', 'price']])
    else:
        print("未找到数据文件，请先运行自动化任务")


def example_scheduling():
    """定时任务示例"""
    print("=== 定时任务示例 ===")
    print("可以使用以下方式实现定时执行:")
    print()
    print("1. Linux/Mac crontab:")
    print("   # 每天早上9点执行")
    print("   0 9 * * * cd /path/to/tiktok_shop_automation && python main.py")
    print()
    print("2. Windows 任务计划程序:")
    print("   创建基本任务，设置触发器和操作")
    print()
    print("3. Python schedule库:")
    print("   pip install schedule")
    print()
    print("   示例代码:")
    print("""
    import schedule
    import time
    from main import TikTokShopAutomation

    def job():
        automation = TikTokShopAutomation()
        automation.run()

    # 每天9点执行
    schedule.every().day.at("09:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(60)
    """)


def main():
    """主函数"""
    print("TikTok店铺自动化 - 使用示例")
    print("=" * 50)
    print()

    examples = {
        '1': ('基本使用', example_basic_usage),
        '2': ('自定义配置', example_custom_config),
        '3': ('数据处理', example_data_processing),
        '4': ('定时任务说明', example_scheduling),
    }

    print("请选择示例:")
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")
    print("  q. 退出")
    print()

    choice = input("请输入选项 (1-4, q): ").strip()

    if choice in examples:
        name, func = examples[choice]
        print()
        func()
    elif choice.lower() == 'q':
        print("退出")
    else:
        print("无效选项")


if __name__ == '__main__':
    # 直接运行数据处理示例（如果有数据的话）
    example_data_processing()

    # 或者运行交互式菜单
    # main()
