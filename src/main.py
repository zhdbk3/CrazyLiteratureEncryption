#
# Created by MC着火的冰块 on 2024/9/22
#

import sys

from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, FluentTranslator
from qfluentwidgets import FluentIcon as FIF

from gui import *

__version__ = '0.1'


class Window(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'发疯文学加密 {__version__}')
        self.resize(800, 600)

        # 添加子界面
        self.interface_settings = InterfaceSettings(self)
        self.addSubInterface(self.interface_settings, FIF.SETTING, '设置')
        self.interface_encrypt = InterfaceEncrypt(self)
        self.addSubInterface(self.interface_encrypt, FIF.VPN, '加密')
        self.interface_decrypt = InterfaceDecrypt(self)
        self.addSubInterface(self.interface_decrypt, FIF.SYNC, '解密')


if __name__ == '__main__':  # 不要删掉这个 if，否则会发生非常恐怖的事情
    app = QApplication(sys.argv)
    translator = FluentTranslator()
    app.installTranslator(translator)
    w = Window()
    w.show()
    sys.exit(app.exec())
