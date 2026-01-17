"""
TikTok店铺自动化主程序
实现自动登录、商品机会热门商品列表抓取功能
"""

import os
import sys
import time
import argparse
from typing import List, Dict, Any, Optional
from loguru import logger

from utils import setup_logger, load_config, BrowserAutomation, DataStorage


class TikTokShopAutomation:
    """TikTok店铺自动化类"""

    def __init__(self, config_path: str = None):
        """
        初始化

        Args:
            config_path: 配置文件路径
        """
        # 加载配置
        self.config = load_config(config_path)

        # 设置日志
        self.logger = setup_logger(self.config.get('logging', {}))

        # 获取配置
        self.shop_config = self.config.get('tiktok_shop', {})
        self.scraping_config = self.config.get('scraping', {})
        self.advanced_config = self.config.get('advanced', {})

        # 初始化组件
        self.browser = None
        self.storage = DataStorage(self.config)

        # 统计信息
        self.total_products = 0
        self.current_page = 0

    def run(self):
        """运行自动化流程"""
        try:
            logger.info("开始执行 TikTok 店铺自动化任务")

            # 初始化浏览器
            with BrowserAutomation(self.config) as browser:
                self.browser = browser

                # 1. 登录
                if not self.login():
                    logger.error("登录失败，终止任务")
                    return False

                # 2. 导航到热门商品页面
                if not self.navigate_to_popular_products():
                    logger.error("导航到热门商品页面失败，终止任务")
                    return False

                # 3. 抓取热门商品数据
                self.scrape_popular_products()

                # 4. 保存数据
                if self.storage.get_buffer_size() > 0:
                    # 去重
                    if self.scraping_config.get('deduplicate', True):
                        self.storage.deduplicate('product_id')

                    filepath = self.storage.save()
                    logger.success(f"数据保存成功: {filepath}")
                    logger.success(f"总计抓取 {self.total_products} 个商品")
                else:
                    logger.warning("没有抓取到任何数据")

            logger.success("TikTok 店铺自动化任务完成")
            return True

        except KeyboardInterrupt:
            logger.warning("用户中断任务")
            return False
        except Exception as e:
            logger.exception(f"任务执行出错: {e}")
            return False

    def login(self) -> bool:
        """
        登录TikTok店铺

        Returns:
            是否登录成功
        """
        logger.info("开始登录 TikTok 店铺...")

        try:
            login_url = self.shop_config.get('login_url')
            username = self.shop_config.get('username')
            password = self.shop_config.get('password')

            if not username or not password:
                logger.error("未配置用户名或密码")
                return False

            # 导航到登录页面
            self.browser.navigate(login_url)
            self.browser.screenshot('01_login_page')

            logger.info("请在浏览器中手动完成登录...")
            logger.info("登录后，程序将自动继续执行")

            # 等待用户登录
            # 这里可以添加更智能的检测逻辑
            # 例如检测特定元素是否出现来判断是否登录成功

            if self.browser.browser_type == 'playwright':
                # 等待登录成功的标志（例如URL变化或特定元素出现）
                # 这里简单等待用户操作
                input("请在浏览器中完成登录，然后按回车键继续...")

            elif self.browser.browser_type == 'selenium':
                input("请在浏览器中完成登录，然后按回车键继续...")

            elif self.browser.browser_type == 'yingdao':
                # 如果使用影刀，可能有自动填充功能
                # 这里保留手动登录逻辑
                input("请在浏览器中完成登录，然后按回车键继续...")

            self.browser.screenshot('02_after_login')
            logger.success("登录完成")

            return True

        except Exception as e:
            logger.error(f"登录过程出错: {e}")
            self.browser.screenshot('error_login')
            return False

    def navigate_to_popular_products(self) -> bool:
        """
        导航到热门商品页面

        Returns:
            是否导航成功
        """
        logger.info("导航到热门商品页面...")

        try:
            shop_url = self.shop_config.get('shop_url')
            popular_path = self.scraping_config.get('popular_products_path', '/product/opportunities/popular')

            # 构建完整URL
            popular_url = f"{shop_url}{popular_path}"

            # 导航
            self.browser.navigate(popular_url)
            self.browser.screenshot('03_popular_products_page')

            logger.success("成功导航到热门商品页面")
            return True

        except Exception as e:
            logger.error(f"导航失败: {e}")
            self.browser.screenshot('error_navigation')
            return False

    def scrape_popular_products(self):
        """
        抓取热门商品数据（瀑布流）
        """
        logger.info("开始抓取热门商品数据...")

        max_pages = self.scraping_config.get('max_pages', 0)
        scrolls_per_page = self.scraping_config.get('scrolls_per_page', 5)
        scroll_pixels = self.scraping_config.get('scroll_pixels', 800)

        try:
            last_height = 0
            no_new_content_count = 0
            page_count = 0

            while True:
                # 检查是否达到最大页数
                if max_pages > 0 and page_count >= max_pages:
                    logger.info(f"已达到最大页数限制: {max_pages}")
                    break

                page_count += 1
                logger.info(f"正在处理第 {page_count} 页...")

                # 滚动加载更多内容
                for i in range(scrolls_per_page):
                    logger.debug(f"滚动 {i + 1}/{scrolls_per_page}")
                    self.browser.scroll_to_bottom(scroll_pixels)

                    # 抓取当前可见的商品
                    products = self.extract_products_from_page()
                    if products:
                        self.storage.add_batch(products)
                        self.total_products += len(products)
                        logger.info(f"本次抓取到 {len(products)} 个商品，总计: {self.total_products}")

                # 检查页面高度是否变化
                current_height = self.browser.get_page_height()
                if current_height == last_height:
                    no_new_content_count += 1
                    logger.debug(f"页面高度未变化 ({no_new_content_count} 次)")

                    if no_new_content_count >= 3:
                        logger.info("已到达页面底部，没有更多内容")
                        break
                else:
                    no_new_content_count = 0
                    last_height = current_height

                # 截图记录
                if page_count % 5 == 0:
                    self.browser.screenshot(f'04_page_{page_count}')

                # 稍作等待
                self.browser.wait(1)

            logger.info(f"抓取完成，共处理 {page_count} 页")

        except Exception as e:
            logger.error(f"抓取过程出错: {e}")
            self.browser.screenshot('error_scraping')

    def extract_products_from_page(self) -> List[Dict[str, Any]]:
        """
        从当前页面提取商品数据

        Returns:
            商品数据列表
        """
        products = []

        try:
            if self.browser.browser_type == 'playwright':
                products = self._extract_with_playwright()
            elif self.browser.browser_type == 'selenium':
                products = self._extract_with_selenium()
            elif self.browser.browser_type == 'yingdao':
                products = self._extract_with_yingdao()

        except Exception as e:
            logger.debug(f"提取商品数据时出错: {e}")

        return products

    def _extract_with_playwright(self) -> List[Dict[str, Any]]:
        """使用 Playwright 提取商品数据"""
        products = []

        try:
            # 这里需要根据 TikTok Shop 的实际页面结构来定位元素
            # 以下是一个示例模板，需要根据实际情况调整选择器

            # 等待商品列表加载
            self.browser.page.wait_for_selector('[data-testid="product-item"], .product-card, .product-item', timeout=5000)

            # 获取所有商品卡片
            # 注意：这些选择器是示例，需要根据实际页面调整
            product_elements = self.browser.page.query_selector_all(
                '[data-testid="product-item"], .product-card, .product-item, [class*="product"]'
            )

            for element in product_elements:
                try:
                    product_data = {}

                    # 提取商品ID
                    product_id = element.get_attribute('data-product-id') or element.get_attribute('id')
                    if product_id:
                        product_data['product_id'] = product_id

                    # 提取商品名称
                    name_elem = element.query_selector('[class*="name"], [class*="title"], h3, h4')
                    if name_elem:
                        product_data['product_name'] = name_elem.inner_text().strip()

                    # 提取价格
                    price_elem = element.query_selector('[class*="price"], [class*="Price"]')
                    if price_elem:
                        product_data['price'] = price_elem.inner_text().strip()

                    # 提取销量
                    sales_elem = element.query_selector('[class*="sales"], [class*="sold"]')
                    if sales_elem:
                        product_data['sales'] = sales_elem.inner_text().strip()

                    # 提取图片URL
                    img_elem = element.query_selector('img')
                    if img_elem:
                        product_data['image_url'] = img_elem.get_attribute('src')

                    # 提取商品链接
                    link_elem = element.query_selector('a')
                    if link_elem:
                        product_data['product_url'] = link_elem.get_attribute('href')

                    # 只添加有效数据
                    if product_data.get('product_id') or product_data.get('product_name'):
                        products.append(product_data)

                except Exception as e:
                    logger.debug(f"提取单个商品数据失败: {e}")
                    continue

        except Exception as e:
            logger.debug(f"Playwright 提取失败: {e}")

        return products

    def _extract_with_selenium(self) -> List[Dict[str, Any]]:
        """使用 Selenium 提取商品数据"""
        products = []

        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            # 等待商品列表加载
            wait = WebDriverWait(self.browser.driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="product-item"], .product-card, .product-item')))

            # 获取所有商品卡片
            product_elements = self.browser.driver.find_elements(By.CSS_SELECTOR, '[data-testid="product-item"], .product-card, .product-item')

            for element in product_elements:
                try:
                    product_data = {}

                    # 提取商品数据（类似 Playwright 的逻辑）
                    product_id = element.get_attribute('data-product-id') or element.get_attribute('id')
                    if product_id:
                        product_data['product_id'] = product_id

                    # 其他字段提取逻辑...
                    if product_data.get('product_id'):
                        products.append(product_data)

                except Exception as e:
                    logger.debug(f"提取单个商品数据失败: {e}")
                    continue

        except Exception as e:
            logger.debug(f"Selenium 提取失败: {e}")

        return products

    def _extract_with_yingdao(self) -> List[Dict[str, Any]]:
        """使用影刀 RPA 提取商品数据"""
        products = []

        try:
            # 影刀RPA的元素定位和数据提取
            # 需要根据影刀的实际API调整
            # 这里提供一个基本框架

            # 示例：使用影刀的元素查找功能
            # product_elements = self.browser.driver.find_elements("商品卡片")

            # for element in product_elements:
            #     product_data = {
            #         'product_id': element.get_attribute('id'),
            #         'product_name': element.find_element('商品名称').text,
            #         # ...
            #     }
            #     products.append(product_data)

            logger.warning("影刀 RPA 数据提取功能需要根据实际SDK实现")

        except Exception as e:
            logger.debug(f"影刀 RPA 提取失败: {e}")

        return products


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='TikTok店铺自动化工具')
    parser.add_argument('-c', '--config', type=str, help='配置文件路径')
    args = parser.parse_args()

    # 创建并运行自动化任务
    automation = TikTokShopAutomation(config_path=args.config)
    success = automation.run()

    # 返回退出码
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
