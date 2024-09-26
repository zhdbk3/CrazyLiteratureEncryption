#
# Created by MC着火的冰块 on 2024/9/21
#

import jieba


class Dictionary:
    def __init__(self):
        # 存储 dict.txt 中的内容，每个元组为 (词语, 词频, 词性)
        self._lines: list[tuple[str, int, str]] = self._init_lines()

        # 按词性划分词库，键为词性，值为该词性的词的列表
        self.parts: dict[str, list[str]] = self._init_parts()

        # 存放各个词出现的概率
        self.p: dict[str, float] = self._init_p()

        # 释放不必要的内存
        del self._lines

    @staticmethod
    def _init_lines() -> list:
        lines = []
        dict_path = jieba.__path__[0] + '/dict.txt'
        with open(dict_path, encoding='utf-8') as f:
            for line in f.readlines():
                word, freq, flag = line.split()
                lines.append((word, int(freq), flag))
        return lines

    def _init_parts(self) -> dict:
        parts = {}
        for word, _, flag in self._lines:
            if flag not in parts:
                parts[flag] = []
            parts[flag].append(word)
        return parts

    def _init_p(self) -> dict:
        p = {}
        total = sum([i[1] for i in self._lines])
        for word, freq, _ in self._lines:
            p[word] = freq / total
        return p


dictionary = Dictionary()
