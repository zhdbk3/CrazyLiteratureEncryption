#
# Created by MC着火的冰块 on 2024/9/16
#

from typing import Never

import jieba

from generate_mapping import MappingGenerator


class Encryptor:
    def __init__(self, seed: int, chunk_size: int):
        """
        发疯文学加密与解密器
        :param seed: 见 MappingGenerator 文档
        :param chunk_size: 见 MappingGenerator 文档
        """
        self.seed = seed
        self.chunk_size = chunk_size
        self.encryption_mapping = MappingGenerator(seed, chunk_size).get_mapping()
        self.decryption_mapping = {v: k for k, v in self.encryption_mapping.items()}

    @staticmethod
    def convert(text: str, mapping: dict[str, str]) -> str:
        """
        加密或解密一个文本
        :param text: 文本
        :param mapping: 映射表，这由模式决定
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

    def encrypt(self, plain_text: str) -> str | Never:
        """加密，若失败会报错"""
        cipher_text = self.convert(plain_text, self.encryption_mapping)
        # 检查是否加密成功
        assert self.decrypt(cipher_text) == plain_text, cipher_text
        return cipher_text

    def decrypt(self, cipher_text: str) -> str:
        """解密"""
        return self.convert(cipher_text, self.decryption_mapping)
