"""
日志配置模块
"""

import os
import sys
from loguru import logger
from datetime import datetime


def setup_logger(config: dict):
    """
    设置日志记录器

    Args:
        config: 日志配置字典
    """
    log_dir = config.get('log_dir', './logs')
    log_file = config.get('log_file', 'tiktok_automation.log')
    level = config.get('level', 'INFO')
    retention_days = config.get('retention_days', 7)

    # 创建日志目录
    os.makedirs(log_dir, exist_ok=True)

    # 移除默认处理器
    logger.remove()

    # 添加控制台输出
    logger.add(
        sys.stdout,
        level=level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )

    # 添加文件输出
    log_path = os.path.join(log_dir, log_file)
    logger.add(
        log_path,
        level=level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="500 MB",
        retention=f"{retention_days} days",
        compression="zip",
        encoding="utf-8"
    )

    logger.info("=" * 50)
    logger.info("TikTok店铺自动化系统启动")
    logger.info(f"日志级别: {level}")
    logger.info(f"日志文件: {log_path}")
    logger.info("=" * 50)

    return logger
