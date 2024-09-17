#
# Created by MC着火的冰块 on 2024/9/16
#

import hashlib

from encryption import Encryptor

print('=' * 20, '发疯文学加密器', '=' * 20)
print('请输入种子（字符串）')
seed = int(hashlib.sha256(input('>>> ').encode('utf-8')).hexdigest(), 16)
print(f'整数种子：{seed}')
print('请输入区块长度（不输入为不分块）')
try:
    chunk_size = int(input('>>> '))
except ValueError:
    chunk_size = None
print()

print('初始化加密器...')
encryptor = Encryptor(seed, chunk_size)
print('完成！')
print()

while True:
    print('加密(e) / 解密(d) / 退出(q)')
    mode = input('>>> ')
    match mode:
        case 'e':
            print('请输入要加密的文本')
            text = input('>>> ')
            try:
                print(encryptor.encrypt(text))
            except AssertionError as e:
                print('\033[91m加密失败：密文无法被还原\033[0m')
                print(f'\033[91m{e}\033[0m')
        case 'd':
            print('请输入要解密的文本')
            text = input('>>> ')
            print(encryptor.decrypt(text))
        case 'q':
            print('期待着与您的再次相见！')
            break
        case _:
            print('喵喵喵？')
    print()
