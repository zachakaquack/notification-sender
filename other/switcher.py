from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Switcher(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.switchers: list[tuple[str, QWidget]] = []
        self.main_switcher: tuple[str, QWidget] | None = None

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def setMainSwitch(self, name: str) -> bool:
        for switch in self.switchers:
            if switch[0] == name:
                self.hideAllSwitches()
                self.main_switcher = switch
                self.main_switcher[1].show()
                return True
        else:
            return False

    def addSwitcherFromTuple(self, tup: tuple[str, QWidget]) -> bool:
        return self._addSwitcher(tup[0], tup[1])

    def addSwitcher(self, name: str, widget: QWidget) -> bool:
        return self._addSwitcher(name, widget)

    def _addSwitcher(self, name: str, widget: QWidget) -> bool:
        for switch in self.switchers:
            if switch[0] == name:
                return False
        self.switchers.append((name, widget))

        self.main_layout.addWidget(widget)
        widget.hide()

        if not self.main_switcher:
            self.main_switcher = self.switchers[0]
            self.main_switcher[1].show()

        return True

    def hideAllSwitches(self) -> None:
        for switch in self.switchers:
            switch[1].hide()
        return

    def switchTo(self, name: str) -> bool:
        for switch in self.switchers:
            if switch[0] == name:
                self.hideAllSwitches()
                switch[1].show()
                return True
        else:
            return False
