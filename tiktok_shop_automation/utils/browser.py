"""
浏览器自动化模块
支持 Playwright、Selenium 和 影刀RPA
"""

import os
import time
from typing import Optional, List, Dict, Any
from loguru import logger


class BrowserAutomation:
    """浏览器自动化基类"""

    def __init__(self, config: Dict[str, Any]):
        """
        初始化浏览器自动化

        Args:
            config: 配置字典
        """
        self.config = config
        self.browser_config = config.get('browser', {})
        self.browser_type = self.browser_config.get('type', 'playwright')
        self.headless = self.browser_config.get('headless', False)
        self.timeout = self.browser_config.get('timeout', 30)
        self.page_load_wait = self.browser_config.get('page_load_wait', 3)
        self.scroll_wait = self.browser_config.get('scroll_wait', 2)

        self.driver = None
        self.page = None
        self.browser = None
        self.playwright = None

        # 截图配置
        self.save_screenshots = config.get('advanced', {}).get('save_screenshots', True)
        self.screenshot_dir = config.get('advanced', {}).get('screenshot_dir', './logs/screenshots')
        if self.save_screenshots:
            os.makedirs(self.screenshot_dir, exist_ok=True)

    def initialize(self):
        """初始化浏览器"""
        if self.browser_type == 'playwright':
            self._init_playwright()
        elif self.browser_type == 'selenium':
            self._init_selenium()
        elif self.browser_type == 'yingdao':
            self._init_yingdao()
        else:
            raise ValueError(f"不支持的浏览器类型: {self.browser_type}")

        logger.info(f"浏览器初始化成功: {self.browser_type}")

    def _init_playwright(self):
        """初始化 Playwright"""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise ImportError("请先安装 Playwright: pip install playwright && playwright install")

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        self.page = self.context.new_page()
        self.page.set_default_timeout(self.timeout * 1000)
        logger.info("Playwright 浏览器初始化成功")

    def _init_selenium(self):
        """初始化 Selenium"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
        except ImportError:
            raise ImportError("请先安装 Selenium: pip install selenium webdriver-manager")

        options = Options()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--window-size=1920,1080')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.set_page_load_timeout(self.timeout)
        logger.info("Selenium 浏览器初始化成功")

    def _init_yingdao(self):
        """初始化影刀RPA"""
        try:
            # 影刀RPA的导入方式可能因版本而异
            # 这里提供一个基本框架，需要根据实际的影刀SDK调整
            import shadowbot  # 这是示例，实际包名可能不同
            self.driver = shadowbot.Browser()
            logger.info("影刀RPA 浏览器初始化成功")
        except ImportError:
            logger.warning("影刀RPA SDK 未安装，请从影刀官网下载并安装")
            logger.warning("将回退使用 Playwright")
            self.browser_type = 'playwright'
            self._init_playwright()

    def navigate(self, url: str):
        """
        导航到指定URL

        Args:
            url: 目标URL
        """
        logger.info(f"导航到: {url}")

        if self.browser_type == 'playwright':
            self.page.goto(url, wait_until='domcontentloaded')
        elif self.browser_type == 'selenium':
            self.driver.get(url)
        elif self.browser_type == 'yingdao':
            self.driver.navigate(url)

        time.sleep(self.page_load_wait)

    def screenshot(self, name: str):
        """
        截图

        Args:
            name: 截图文件名
        """
        if not self.save_screenshots:
            return

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.screenshot_dir, f"{name}_{timestamp}.png")

        try:
            if self.browser_type == 'playwright':
                self.page.screenshot(path=filepath, full_page=True)
            elif self.browser_type == 'selenium':
                self.driver.save_screenshot(filepath)
            elif self.browser_type == 'yingdao':
                self.driver.screenshot(filepath)

            logger.debug(f"截图保存: {filepath}")
        except Exception as e:
            logger.warning(f"截图失败: {e}")

    def scroll_to_bottom(self, pixels: int = 800):
        """
        向下滚动页面

        Args:
            pixels: 滚动像素数
        """
        if self.browser_type == 'playwright':
            self.page.evaluate(f"window.scrollBy(0, {pixels})")
        elif self.browser_type == 'selenium':
            self.driver.execute_script(f"window.scrollBy(0, {pixels})")
        elif self.browser_type == 'yingdao':
            self.driver.scroll(0, pixels)

        time.sleep(self.scroll_wait)

    def get_page_height(self) -> int:
        """获取页面高度"""
        if self.browser_type == 'playwright':
            return self.page.evaluate("document.body.scrollHeight")
        elif self.browser_type == 'selenium':
            return self.driver.execute_script("return document.body.scrollHeight")
        elif self.browser_type == 'yingdao':
            return self.driver.execute_script("return document.body.scrollHeight")
        return 0

    def wait(self, seconds: float):
        """等待指定秒数"""
        time.sleep(seconds)

    def close(self):
        """关闭浏览器"""
        try:
            if self.browser_type == 'playwright':
                if self.page:
                    self.page.close()
                if self.context:
                    self.context.close()
                if self.browser:
                    self.browser.close()
                if self.playwright:
                    self.playwright.stop()
            elif self.browser_type == 'selenium':
                if self.driver:
                    self.driver.quit()
            elif self.browser_type == 'yingdao':
                if self.driver:
                    self.driver.close()

            logger.info("浏览器已关闭")
        except Exception as e:
            logger.error(f"关闭浏览器时出错: {e}")

    def __enter__(self):
        """上下文管理器入口"""
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.close()
