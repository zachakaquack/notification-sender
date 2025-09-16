from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from other import file_management
from other.notification_class import Notification


class BlankNotificationWidget(QFrame):

    notificationCreated = Signal(Notification)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setMinimumSize(200, 200)
        self.setObjectName("notification-widget")
        self.setStyleSheet(
            """
            #notification-widget{
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #303030;
                border-radius: 5px
            }
            QLabel{
                color: #303030;
            }
            """
        )

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(5)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("+")
        self.label.setFont(QFont("Calibri", 64))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.label.mousePressEvent = self.clicked

        self.main_layout.addWidget(self.label)

    def clicked(self, _) -> None:
        n = file_management.create_new_notification()
        self.notificationCreated.emit(n)
