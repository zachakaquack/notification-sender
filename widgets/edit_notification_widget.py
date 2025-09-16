from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from other import file_management
from other.notification_class import Notification


class EditNotificationWidget(QFrame):

    back = Signal(Notification)
    delete = Signal(Notification)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.notification = None
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet(
            """
            color: white;
            """
        )

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        self.top_bar = None

    def load_notification(self, notification: Notification) -> None:
        self.notification = notification

        self.create_groupboxes()

        self.top_bar = TopBar()
        self.top_bar.back.connect(lambda: self.back.emit(self.notification))
        self.top_bar.delete.connect(lambda: self.delete.emit(self.notification))
        self.main_layout.insertWidget(0, self.top_bar)
        self.top_bar.load(notification)

    def create_groupboxes(self) -> None:

        while (child := self.main_layout.takeAt(0)) != None:
            if (
                child.widget()
                and isinstance(child.widget(), EditorBasic)
                or child.widget()
                and isinstance(child.widget(), NumericalEditor)
            ):
                child.widget().deleteLater()

        self.app_name_gb = EditorBasic("App Name", "app_name")
        self.replaces_id = NumericalEditor("Replaces ID", "replaces_id")
        self.app_icon = EditorBasic("App Icon", "app_icon")
        self.title = EditorBasic("Title Name", "title")
        self.body = EditorBasic("Body", "body")
        self.duration = NumericalEditor("Duration (ms)", "duration")

        for gb in [
            self.app_name_gb,
            self.replaces_id,
            self.app_icon,
            self.title,
            self.body,
            self.duration,
        ]:
            self.main_layout.addWidget(gb)
            gb.textChanged.connect(self.update_class)
            gb.load_default_value(self.notification)

    def update_class(self, json_key, value) -> None:
        if self.notification:
            file_management.edit_notification(self.notification.index, json_key, value)
            d = self.notification.to_dict()
            d[json_key] = value
            self.notification.from_dict(d)
            if f"{json_key}" == "title" and self.top_bar:
                self.top_bar.title_label.setText(value)


class EditorBasic(QGroupBox):

    textChanged = Signal(str, str)

    def __init__(self, title, json_key, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.title = title
        self.json_key = json_key

        self.setMaximumHeight(100)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(5)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.setObjectName("gb")
        self.setStyleSheet(
            """
            #gb{
                border-radius: 5px;
                border: 1px solid #303030;
            }
            """
        )

        self.label = QLabel(self.title)
        self.main_layout.addWidget(self.label)

        self.input = QLineEdit()
        self.input.setPlaceholderText(f"Enter {self.title}...")
        self.input.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.input.textChanged.connect(
            lambda text: self.textChanged.emit(self.json_key, text)
        )

        self.main_layout.addWidget(self.input)

    def load_default_value(self, notification: Notification) -> None:
        self.input.setText(notification.to_dict()[self.json_key])


class NumericalEditor(QGroupBox):

    textChanged = Signal(str, str)

    def __init__(self, title, json_key, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.title = title
        self.json_key = json_key

        self.setMaximumHeight(100)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(5)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.setObjectName("gb")
        self.setStyleSheet(
            """
            #gb{
                border-radius: 5px;
                border: 1px solid #303030;
            }
            """
        )

        self.label = QLabel(self.title)
        self.main_layout.addWidget(self.label)

        self.input = QSpinBox()
        self.input.setRange(-1, 600000)
        self.input.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.input.textChanged.connect(
            lambda text: self.textChanged.emit(self.json_key, text)
        )
        self.main_layout.addWidget(self.input)

    def load_default_value(self, notification: Notification) -> None:
        self.input.setValue(int(notification.to_dict()[self.json_key]))


class TopBar(QFrame):

    back = Signal()
    delete = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setMaximumHeight(64)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.setObjectName("topbar")
        self.setStyleSheet(
            """
            #topbar{
                border-bottom: 3px solid #303030;
            }
            *{
                background-color: #1e1e1e;
                color: white;
            }
            """
        )

        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
        )

        # back button
        self.back_button = QLabel()
        pm = QIcon("assets/back.svg").pixmap(QSize(32, 32))
        self.back_button.setPixmap(pm)
        self.back_button.setFont(QFont("Calibri", 32))
        self.back_button.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.main_layout.addWidget(self.back_button)
        self.back_button.mouseReleaseEvent = lambda _: self.back.emit()

        # spacer items so it centers
        self.main_layout.addSpacerItem(
            QSpacerItem(1, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)
        )

        self.title_label = QLabel("Title (you shouldn't be seeing this!)")
        self.title_label.setFont(QFont("Calibri", 24))
        self.main_layout.addWidget(self.title_label)

        self.main_layout.addSpacerItem(
            QSpacerItem(1, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)
        )

        self.delete_button = QLabel()
        pm = QIcon("assets/delete.svg").pixmap(QSize(32, 32))
        self.delete_button.setPixmap(pm)
        self.delete_button.setFont(QFont("Calibri", 32))
        self.delete_button.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.main_layout.addWidget(self.delete_button)
        self.delete_button.mouseReleaseEvent = lambda _: self.delete.emit()

    def load(self, notification: Notification) -> None:
        self.title_label.setText(notification.title)
