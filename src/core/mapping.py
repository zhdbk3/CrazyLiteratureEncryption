#
# Created by MC着火的冰块 on 2024/9/16
#

import random
from functools import lru_cache

if __name__ == '__main__':
    from dictionary import dictionary
else:
    from .dictionary import dictionary


class MappingGenerator:
    def __init__(self, seed: int):
        """
        映射表生成器
        :param seed: 基础的随机数种子
        """
        self.seed = seed

    # # 我曾经想通过分块打乱的方式来提高加密成功率，但是实际效果并不理想
    # # 为记录曲折探索的过程，遂保留部分代码
    # def chunk(self, ls: list) -> Iterable[list]:  # list[list]:
    #     """给列表分块"""
    #     # if self.chunk_size is None or len(ls) <= self.chunk_size:
    #     #     return [ls]
    #     # return [ls[:self.chunk_size], *self.chunk(ls[self.chunk_size:])]
    #     # # 可恶...好长的列表...解释器不听使唤了呢♡ 啊啊太深了♡
    #     # # 递归层数...太多了♡ 要...溢出来惹♡
    #     # # RecursionError: maximum recursion depth exceeded
    #     if self.chunk_size is None:
    #         yield ls.copy()
    #     else:
    #         for i in range(0, len(ls), self.chunk_size):
    #             yield ls[i:i + self.chunk_size]

    @lru_cache(1)
    def get(self, offset: int) -> dict[str, str]:
        """
        获取映射表
        会留一次缓存，因为每次尝试加密完都会再解密来检查是否加密成功
        :param offset: 种子的偏移量，在随机打乱前，这将被加到种子上
        :return: 映射表
        """
        mapping = {}
        for flag in dictionary.parts:
            # 获取该词性的词的列表
            keys = dictionary.parts[flag]
            # 打乱
            vals = keys.copy()
            random.seed(self.seed + offset)
            random.shuffle(vals)
            # 加入映射表
            mapping.update(dict(zip(keys, vals)))
        return mapping


if __name__ == '__main__':
    import time

    mg = MappingGenerator(20090513)
    for i in range(10):
        t1 = time.time()
        mg.get(i)
        t2 = time.time()
        print(t2 - t1)
