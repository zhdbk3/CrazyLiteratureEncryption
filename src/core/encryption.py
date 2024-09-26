#
# Created by MC着火的冰块 on 2024/9/16
#

import jieba

from .mapping import MappingGenerator


class Encryptor:
    def __init__(self, seed: int):
        """
        发疯文学加密与解密器
        :param seed: 基础的随机数种子
        """
        self.seed = seed
        self.mg = MappingGenerator(seed)

    @staticmethod
    def convert(text: str, mapping: dict[str, str]) -> str:
        """
        加密或解密一个文本
        :param text: 文本
        :param mapping: 映射表
        :return: 转换后的文本
        """
        result = ''
        words = jieba.cut(text)
        for word in words:
            if word in mapping:
                result += mapping[word]
            else:
                result += word
        return result

    def encrypt(self, plain_text: str, offset: int) -> str:
        """
        按照给定的偏移量加密
        :param plain_text: 明文
        :param offset: 偏移量
        :return: 密文
        """
        mapping = self.mg.get(offset)
        return self.convert(plain_text, mapping)

    def decrypt(self, cipher_text: str, offset: int) -> str:
        """
        按照给定的偏移量解密
        :param cipher_text: 密文
        :param offset: 偏移量
        :return: 明文
        """
        mapping = {v: k for k, v in self.mg.get(offset).items()}
        return self.convert(cipher_text, mapping)
