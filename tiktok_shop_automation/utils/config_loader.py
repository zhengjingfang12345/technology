"""
配置文件加载模块
"""

import os
import yaml
from typing import Dict, Any


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    加载配置文件

    Args:
        config_path: 配置文件路径，默认为 config/config.yaml

    Returns:
        配置字典
    """
    if config_path is None:
        # 获取项目根目录
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(current_dir, 'config', 'config.yaml')

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # 从环境变量读取敏感信息
    if 'TIKTOK_USERNAME' in os.environ:
        config['tiktok_shop']['username'] = os.environ['TIKTOK_USERNAME']
    if 'TIKTOK_PASSWORD' in os.environ:
        config['tiktok_shop']['password'] = os.environ['TIKTOK_PASSWORD']

    return config
