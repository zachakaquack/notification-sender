from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from other import file_management
from other.flow import FlowLayout
from other.notification_class import Notification
from other.switcher import Switcher
from widgets.blank_notification_widget import BlankNotificationWidget
from widgets.notification_widget import NotificationWidget
from widgets.edit_notification_widget import EditNotificationWidget
from widgets.notification_scroller import NotificationScroller


class Interface(QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.widgets = []

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.main_widget = QFrame()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_widget.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        self.switcher = Switcher()
        self.main_layout.addWidget(self.switcher)

        self.edit = EditNotificationWidget()
        self.edit.back.connect(self.switch_to_main)
        self.edit.delete.connect(self.delete_notification)
        self.switcher.addSwitcher("edit", self.edit)

        self.scroller = NotificationScroller()
        self.scroller.editNotification.connect(self.switch_to_edit)
        self.switcher.addSwitcher("main", self.scroller)
        self.switcher.setMainSwitch("main")

        self.setWidget(self.switcher)
        self.setWidgetResizable(True)

    def switch_to_edit(self, notification) -> None:
        self.switcher.switchTo("edit")
        self.edit.load_notification(notification)

    def switch_to_main(self, notification: Notification) -> None:
        self.switcher.switchTo("main")
        self.scroller.widgets[notification.index].reload_icon()

    def delete_notification(self, notification: Notification) -> None:
        file_management.remove_notification(notification.index)
        self.switcher.switchTo("main")
        self.scroller.load_notifications()
