#
# Created by MC着火的冰块 on 2024/9/22
#

from multiprocessing import Process, Queue

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QColor
from qfluentwidgets import FluentIcon as FIF

from .ui_encrypt import Ui_Encrypt
from core.info import info_density
from core.encryption import Encryptor

if __name__ == '__main__':  # 骗代码补全
    from main import Window


class InterfaceEncrypt(QWidget, Ui_Encrypt):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName(self.__class__.__name__)

        self.win: "Window" = parent
        self.thread_encrypt = ThreadEncrypt(self.win)

        self.init_ui()
        self.connect_signals_and_slots()

    def init_ui(self) -> None:
        self.primaryPushButton_encrypt.setIcon(FIF.PLAY)
        self.indeterminateProgressBar.pause()
        self.show_density()

    def connect_signals_and_slots(self) -> None:
        # 文本更改时计算信息密度
        self.plainTextEdit_plain.textChanged.connect(self.show_density)
        # 信息密度判定线变化时重新上色
        self.win.interface_settings.doubleSpinBox_density_level.valueChanged.connect(self.color_the_density)
        # 开始加密
        self.primaryPushButton_encrypt.clicked.connect(self.encrypt)
        # 显示偏移量与密文
        self.thread_encrypt.sig_offset.connect(self.bodyLabel_offset.setText)
        self.thread_encrypt.sig_cipher.connect(self.plainTextEdit_cipher.setPlainText)
        # 加密完成
        self.thread_encrypt.finished.connect(self.encryption_finished)

    def show_density(self) -> None:
        """显示输入明文的信息密度"""
        text = self.plainTextEdit_plain.toPlainText()
        density = info_density(text)
        self.bodyLabel_density.setText(str(density))
        self.color_the_density()

    def color_the_density(self) -> None:
        """给密度上色"""
        density = eval(self.bodyLabel_density.text())
        if density is None:
            self.bodyLabel_density.setTextColor()  # 恢复默认
        elif density <= self.win.interface_settings.doubleSpinBox_density_level.value():
            # 密度小是有效信息
            green = QColor(0, 255, 0)
            self.bodyLabel_density.setTextColor(green, green)
        else:
            # 密度大是无效信息
            red = QColor(255, 0, 0)
            self.bodyLabel_density.setTextColor(red, red)

    def set_enabled_partly(self, enabled: bool) -> None:
        """启用或禁用部分组件"""
        self.win.interface_settings.lineEdit_seed_str.setEnabled(enabled)
        self.primaryPushButton_encrypt.setEnabled(enabled)
        self.plainTextEdit_plain.setReadOnly(not enabled)

    def encrypt(self) -> None:
        """加密，启动！"""
        # 禁用组件
        self.set_enabled_partly(False)
        # 启动进度条
        self.indeterminateProgressBar.resume()
        # 线程，启动！
        self.thread_encrypt.start()

    def encryption_finished(self) -> None:
        """加密完成后要做的事"""
        # 启用组件
        self.set_enabled_partly(True)
        # 停止进度条
        self.indeterminateProgressBar.pause()


class ThreadEncrypt(QThread):
    """这个线程会创建一个子进程来处理加密运算，自己则负责实时显示结果"""
    sig_offset = pyqtSignal(str)  # 显示偏移量，应转化为 str 再发射
    sig_cipher = pyqtSignal(str)  # 显示密文

    def __init__(self, win):
        super().__init__()
        self.win: "Window" = win

    def run(self) -> None:
        # 子进程，启动！
        queue = Queue()
        seed = self.win.interface_settings.seed_int
        plain_text = self.win.interface_encrypt.plainTextEdit_plain.toPlainText()
        process = ProcessEncrypt(queue, seed, plain_text)
        process.start()

        # 实时获取结果
        while True:
            output = queue.get()
            # 根据类型判断传过来的是啥
            if isinstance(output, int):
                self.sig_offset.emit(str(output))
            elif isinstance(output, str):
                self.sig_cipher.emit(output)
                return


class ProcessEncrypt(Process):
    """在子进程中进行加密运算"""

    def __init__(self, queue: Queue, seed: int, plain_text: str):
        super().__init__()
        self.queue = queue
        self.seed = seed
        self.plain_text = plain_text

    def run(self) -> None:
        encryptor = Encryptor(self.seed)
        offset = 0
        while True:
            # 把当前偏移量 (int) 放到管道里
            self.queue.put(offset)

            # 加密
            cipher_text = encryptor.encrypt(self.plain_text, offset)
            # 检查是否加密成功
            if encryptor.decrypt(cipher_text, offset) == self.plain_text:
                # 成功，把结果 (str) 放到管道里
                self.queue.put(cipher_text)
                return

            # 增加偏移量
            offset += 1
