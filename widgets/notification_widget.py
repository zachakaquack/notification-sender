from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from other.notification_class import Notification


class NotificationWidget(QFrame):

    editNotification = Signal(Notification)

    def __init__(self, notification: Notification, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.notification = notification

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
            """
        )

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(15)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        size = 128
        pm = self.notification.get_icon()
        pm = QIcon(pm).pixmap(QSize(size, size))
        if pm.isNull():
            pm = QIcon("assets/error.svg").pixmap(QSize(size, size))
        self.label.setPixmap(pm)

        self.main_layout.addWidget(self.label)

        self.buttons_widget = QFrame()
        self.buttons_layout = QGridLayout(self.buttons_widget)
        self.setLayout(self.buttons_layout)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout.setSpacing(5)
        self.buttons_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        self.main_layout.addWidget(self.buttons_widget)

        self.load_notification_button = self.Button("Launch")
        self.edit_notification_button = self.Button("Edit")

        self.load_notification_button.clicked.connect(self.launch_notification)
        self.edit_notification_button.clicked.connect(self.edit_notification)

        self.buttons_layout.addWidget(self.load_notification_button, 0, 0)
        self.buttons_layout.addWidget(self.edit_notification_button, 0, 1)

    def reload_icon(self) -> None:
        size = 128
        pm = self.notification.get_icon()
        pm = QIcon(pm).pixmap(QSize(size, size))
        if pm.isNull():
            pm = QIcon("assets/error.svg").pixmap(QSize(size, size))
        self.label.setPixmap(pm)

    def launch_notification(self) -> None:
        self.notification.launch_notification()

    def edit_notification(self) -> None:
        self.editNotification.emit(self.notification)

    class Button(QPushButton):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, *kwargs)

            self.setStyleSheet(
                """
                color: white;
                background-color: #303030;
                """
            )
            self.setMinimumWidth(64)
            self.setMinimumHeight(32)
