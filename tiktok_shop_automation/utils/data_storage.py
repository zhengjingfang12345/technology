"""
数据存储模块
支持 JSON、CSV、Excel 格式
"""

import os
import json
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
from loguru import logger


class DataStorage:
    """数据存储类"""

    def __init__(self, config: Dict[str, Any]):
        """
        初始化数据存储

        Args:
            config: 配置字典
        """
        self.config = config
        self.storage_config = config.get('storage', {})
        self.format = self.storage_config.get('format', 'excel')
        self.output_dir = self.storage_config.get('output_dir', './data')
        self.file_prefix = self.storage_config.get('file_prefix', 'tiktok_popular_products')
        self.append = self.storage_config.get('append', False)
        self.timestamp_format = self.storage_config.get('timestamp_format', '%Y%m%d_%H%M%S')

        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)

        self.data_buffer: List[Dict[str, Any]] = []

    def add_data(self, item: Dict[str, Any]):
        """
        添加单条数据到缓冲区

        Args:
            item: 数据项
        """
        self.data_buffer.append(item)
        logger.debug(f"数据已添加到缓冲区，当前缓冲区大小: {len(self.data_buffer)}")

    def add_batch(self, items: List[Dict[str, Any]]):
        """
        批量添加数据到缓冲区

        Args:
            items: 数据项列表
        """
        self.data_buffer.extend(items)
        logger.info(f"批量添加 {len(items)} 条数据，当前缓冲区大小: {len(self.data_buffer)}")

    def save(self, filename: str = None) -> str:
        """
        保存数据到文件

        Args:
            filename: 文件名（可选，默认使用时间戳）

        Returns:
            保存的文件路径
        """
        if not self.data_buffer:
            logger.warning("缓冲区为空，没有数据需要保存")
            return None

        # 生成文件名
        if filename is None:
            timestamp = datetime.now().strftime(self.timestamp_format)
            filename = f"{self.file_prefix}_{timestamp}"

        # 根据格式保存
        if self.format == 'json':
            filepath = self._save_json(filename)
        elif self.format == 'csv':
            filepath = self._save_csv(filename)
        elif self.format == 'excel':
            filepath = self._save_excel(filename)
        else:
            raise ValueError(f"不支持的存储格式: {self.format}")

        logger.info(f"数据已保存: {filepath} ({len(self.data_buffer)} 条记录)")

        # 清空缓冲区
        self.data_buffer.clear()

        return filepath

    def _save_json(self, filename: str) -> str:
        """保存为JSON格式"""
        filepath = os.path.join(self.output_dir, f"{filename}.json")

        # 如果需要追加且文件存在
        if self.append and os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                if isinstance(existing_data, list):
                    existing_data.extend(self.data_buffer)
                    data_to_save = existing_data
                else:
                    data_to_save = self.data_buffer
            except:
                data_to_save = self.data_buffer
        else:
            data_to_save = self.data_buffer

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)

        return filepath

    def _save_csv(self, filename: str) -> str:
        """保存为CSV格式"""
        filepath = os.path.join(self.output_dir, f"{filename}.csv")

        df = pd.DataFrame(self.data_buffer)

        # 如果需要追加且文件存在
        if self.append and os.path.exists(filepath):
            df.to_csv(filepath, mode='a', header=False, index=False, encoding='utf-8-sig')
        else:
            df.to_csv(filepath, index=False, encoding='utf-8-sig')

        return filepath

    def _save_excel(self, filename: str) -> str:
        """保存为Excel格式"""
        filepath = os.path.join(self.output_dir, f"{filename}.xlsx")

        df = pd.DataFrame(self.data_buffer)

        # 如果需要追加且文件存在
        if self.append and os.path.exists(filepath):
            try:
                existing_df = pd.read_excel(filepath)
                df = pd.concat([existing_df, df], ignore_index=True)
            except:
                pass

        # 使用 openpyxl 引擎保存
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='TikTok热门商品')

        return filepath

    def get_buffer_size(self) -> int:
        """获取缓冲区大小"""
        return len(self.data_buffer)

    def clear_buffer(self):
        """清空缓冲区"""
        self.data_buffer.clear()
        logger.debug("缓冲区已清空")

    def deduplicate(self, key: str = 'product_id'):
        """
        去重

        Args:
            key: 用于去重的字段名
        """
        before_count = len(self.data_buffer)

        # 使用字典去重，保持顺序
        seen = set()
        deduplicated = []
        for item in self.data_buffer:
            if key in item and item[key] not in seen:
                seen.add(item[key])
                deduplicated.append(item)

        self.data_buffer = deduplicated
        after_count = len(self.data_buffer)

        removed = before_count - after_count
        if removed > 0:
            logger.info(f"去重完成: 移除 {removed} 条重复数据")
