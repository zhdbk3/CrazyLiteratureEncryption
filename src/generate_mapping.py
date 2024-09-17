#
# Created by MC着火的冰块 on 2024/9/16
#

import os
import random
from typing import Optional, Iterable


class MappingGenerator:
    def __init__(self, seed: int, chunk_size: Optional[int] = None):
        """
        映射表生成器
        :param seed: 随机数种子
        :param chunk_size: 打乱词库时的区块大小，每个区块会被单独打乱
                           None 为不分块
                           降低它可以提升加密成功率，但同时也会降低熵
        """
        self.seed = seed
        self.chunk_size = chunk_size

    def chunk(self, ls: list) -> Iterable[list]:  # list[list]:
        """给列表分块"""
        # if self.chunk_size is None or len(ls) <= self.chunk_size:
        #     return [ls]
        # return [ls[:self.chunk_size], *self.chunk(ls[self.chunk_size:])]
        # # 可恶...好长的列表...解释器不听使唤了呢♡ 啊啊太深了♡
        # # 递归层数...太多了♡ 要...溢出来惹♡
        # # RecursionError: maximum recursion depth exceeded
        if self.chunk_size is None:
            yield ls.copy()
        else:
            for i in range(0, len(ls), self.chunk_size):
                yield ls[i:i + self.chunk_size]

    def shuffle(self, ls: list) -> list:
        """分块打乱列表"""
        result = []
        for chunk in self.chunk(ls):
            random.seed(self.seed)
            random.shuffle(chunk)
            result.extend(chunk)
        return result

    def get_mapping(self) -> dict[str, str]:
        """获取映射表"""
        result = {}
        for name in os.listdir('parts'):
            # 读取该词性的词库
            with open(f'parts/{name}', encoding='utf-8') as f:
                keys = f.read().split('\n')
                # 分块打乱
                vals = self.shuffle(keys)
                # 加入映射表
                result.update(dict(zip(keys, vals)))
        print(f'映射了 {len(result)} 个词')
        return result
