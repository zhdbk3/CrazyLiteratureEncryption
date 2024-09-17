#
# Created by MC着火的冰块 on 2024/9/16
#

"""
按词性拆分 jieba 的词库
生成的每个文件都是按词频从高到低排列的
"""

import jieba

# 获取词库路径
dict_path = jieba.__file__.replace('__init__.py', 'dict.txt')
print('词库路径', dict_path)

# 读取字典内容
with open(dict_path, encoding='utf-8') as f:
    lines = f.readlines()

# {词性: [(词语, 词频), ...], ...}
# 应按词频从大到小排列
parts: dict[str, list[tuple[str, int]]] = {}

# 分类写入 parts，先不排序
for line in lines:
    word, frequency, flag = line.split()  # 词语, 词频, 词性
    frequency = int(frequency)
    if flag not in parts:
        parts[flag] = []
    parts[flag].append((word, frequency))

# 按词频排序
for flag in parts:
    parts[flag] = sorted(parts[flag], key=lambda x: x[1], reverse=True)

# 写入文件
for flag, words in parts.items():
    with open(f'../src/jieba/parts/{flag}.txt', 'w', encoding='utf-8') as f:
        print(f'词性 {flag:^4} 共有 {len(words):>6} 个词')
        f.write('\n'.join([line[0] for line in words]))
