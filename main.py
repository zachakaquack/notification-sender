from rich.traceback import install
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import qdarktheme
import sys

install()

from widgets.interface import Interface


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #1e1e1e;")

        self.interface = Interface()

        self.setCentralWidget(self.interface)

    def keyPressEvent(self, event: QKeyEvent, /) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.close()

        return super().keyPressEvent(event)


app = QApplication(sys.argv)
qdarktheme.load_stylesheet()
w = MainWindow()
w.show()
sys.exit(app.exec())
