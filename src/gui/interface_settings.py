#
# Created by MC着火的冰块 on 2024/9/22
#

import hashlib
import sys

from PyQt5.QtWidgets import QWidget
import jieba

from .ui_settings import Ui_Settings


class InterfaceSettings(QWidget, Ui_Settings):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName(self.__class__.__name__)

        self.seed_int = None  # 整数种子

        self.init_ui()
        self.connect_signals_and_slots()

    def init_ui(self) -> None:
        self.calc_seed_int()
        self.bodyLabel_python_version.setText(sys.version)
        self.bodyLabel_jieba_version.setText(f'jieba {jieba.__version__}')

    def connect_signals_and_slots(self) -> None:
        # 字符串种子变化时计算整数种子
        self.lineEdit_seed_str.textChanged.connect(self.calc_seed_int)

    def calc_seed_int(self) -> None:
        """对字符串种子进行 SHA-256 得到整数种子并显示"""
        seed_str = self.lineEdit_seed_str.text()
        seed_int = int(hashlib.sha256(seed_str.encode('utf-8')).hexdigest(), 16)
        self.bodyLabel_seed_int.setText(str(seed_int))
        self.seed_int = seed_int
