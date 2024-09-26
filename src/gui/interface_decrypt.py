#
# Created by MC着火的冰块 on 2024/9/22
#

from multiprocessing import Process, Queue, Value

from PyQt5.QtWidgets import QWidget, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QColor
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import PlainTextEdit

from .ui_decrypt import Ui_Decrypt
from core.encryption import Encryptor
from core.info import info_density

if __name__ == '__main__':
    from main import Window


class InterfaceDecrypt(QWidget, Ui_Decrypt):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName(self.__class__.__name__)

        self.win: "Window" = parent
        self.thread_decrypt = ThreadDecrypt(self.win)

        self.init_ui()
        self.connect_signals_and_slots()

    def init_ui(self) -> None:
        # 设置按钮图标
        self.primaryPushButton_decrypt.setIcon(FIF.PLAY)
        # 停止进度环
        self.indeterminateProgressRing.stop()
        # 拉伸表格第一列
        self.tableWidget_results.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

    def connect_signals_and_slots(self) -> None:
        # 开始解密
        self.primaryPushButton_decrypt.clicked.connect(self.decrypt)
        # 解密完成
        self.thread_decrypt.finished.connect(self.decryption_finished)
        # 更新表格
        self.thread_decrypt.sig_update.connect(self.update_table)
        # 密度判定线变化时重新上色
        self.win.interface_settings.doubleSpinBox_density_level.valueChanged.connect(self.color_the_densities)

    def set_enabled_partly(self, enabled: bool) -> None:
        """启用或禁用部分组件"""
        self.win.interface_settings.lineEdit_seed_str.setEnabled(enabled)
        self.primaryPushButton_decrypt.setEnabled(enabled)
        self.plainTextEdit_cipher.setReadOnly(not enabled)

    def decrypt(self) -> None:
        """jiemi（划掉）DCL（划掉）解密，启动！"""
        # 禁用组件
        self.set_enabled_partly(False)
        # 启动进度环
        self.indeterminateProgressRing.start()
        # 启动解密线程
        self.thread_decrypt.start()

    def decryption_finished(self) -> None:
        """解密完成后要做的事"""
        # 启用组件
        self.set_enabled_partly(True)
        # 停止进度环
        self.indeterminateProgressRing.stop()

    def update_table(self, results: list[tuple[str, float | None, int]]) -> None:
        """
        更新表格
        :param results: [(明文, 信息密度, 偏移量), ...]
        :return: None
        """
        # 按信息密度升序排列，None 放最后
        results = sorted(results, key=lambda x: x[1] if x[1] is not None else float('inf'))
        # 填入表格
        self.tableWidget_results.setRowCount(len(results))
        for i in range(len(results)):
            for j in range(3):
                if j == 0:
                    # 在 PlainTextEdit 里显示文本
                    edit = PlainTextEdit()
                    edit.setPlainText(results[i][j])
                    edit.setReadOnly(True)
                    edit.setFixedHeight(100)
                    self.tableWidget_results.setCellWidget(i, j, edit)
                else:
                    item = QTableWidgetItem(str(results[i][j]))
                    self.tableWidget_results.setItem(i, j, item)
        # 调整表格尺寸
        self.tableWidget_results.resizeColumnsToContents()
        self.tableWidget_results.resizeRowsToContents()
        # 上色
        self.color_the_densities()
        # 拉伸表格
        self.tableWidget_results.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

    def color_the_densities(self) -> None:
        """给表格里所有的密度上色"""
        for i in range(self.tableWidget_results.rowCount()):
            item = self.tableWidget_results.item(i, 1)
            density = eval(item.text())
            if density is None:
                continue
            elif density <= self.win.interface_settings.doubleSpinBox_density_level.value():
                # 密度小是有效信息
                color = QColor(0, 255, 0)  # 绿色
            else:
                # 密度大是无效信息
                color = QColor(255, 0, 0)  # 红色
            item.setForeground(color)


class ThreadDecrypt(QThread):
    """创建一个子线程解密，自己负责显示结果"""
    sig_update = pyqtSignal(list)  # 更新表格

    def __init__(self, win):
        super().__init__()
        self.win: "Window" = win

    def run(self) -> None:
        # 启动子进程
        queue = Queue()
        seed = self.win.interface_settings.seed_int
        cipher_text = self.win.interface_decrypt.plainTextEdit_cipher.toPlainText()
        density_level = Value('f')  # 创建共享内存
        density_level.value = self.win.interface_settings.doubleSpinBox_density_level.value()
        process = ProcessDecrypt(queue, seed, cipher_text, density_level)
        process.start()

        results = []
        while True:
            # 更新判定线
            density_level.value = self.win.interface_settings.doubleSpinBox_density_level.value()
            # 获取结果
            output = queue.get()
            if output is None:  # 结束信号
                return
            else:
                results.append(output)
                self.sig_update.emit(results)


class ProcessDecrypt(Process):
    """解密进程"""

    def __init__(self, queue: Queue, seed: int, cipher_text: str, density_level: Value):
        super().__init__()
        self.queue = queue
        self.seed = seed
        self.cipher_text = cipher_text
        self.density_level = density_level

    def run(self) -> None:
        encryptor = Encryptor(self.seed)

        # 从偏移 0 开始尝试
        offset = 0
        while True:
            # 解密
            plain_text = encryptor.decrypt(self.cipher_text, offset)
            # 计算信息密度
            density = info_density(plain_text)
            # 发送结果
            self.queue.put((plain_text, density, offset))
            # 检查是否满足信息密度要求
            if density is not None:
                if density <= self.density_level.value:
                    self.queue.put(None)  # None 代表完成
                    return
            offset += 1
