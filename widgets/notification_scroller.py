from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from other import file_management
from other.flow import FlowLayout
from other.notification_class import Notification
from widgets.blank_notification_widget import BlankNotificationWidget
from widgets.notification_widget import NotificationWidget


class NotificationScroller(QScrollArea):

    editNotification = Signal(Notification)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.widgets = []

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setObjectName("interface")
        self.setStyleSheet(
            """
            #interface {
                background-color: #1e1e1e;
                color: white;
            }
            """
        )

        # switch between the main layout (showing every notification)
        # and the area to edit the widget

        self.main_widget = QFrame()
        self.main_layout = FlowLayout(self.main_widget)
        self.main_widget.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)

        self.load_notifications()

    def load_notifications(self) -> None:

        while (child := self.main_layout.takeAt(0)) != None:
            if child.widget() and isinstance(child.widget(), NotificationWidget):
                child.widget().deleteLater()
            elif child.widget() and isinstance(child.widget(), BlankNotificationWidget):
                child.widget().deleteLater()

        self.widgets = []

        notifications = file_management.get_notifications()
        for notification in notifications:
            widget = NotificationWidget(notification)
            widget.editNotification.connect(self.edit_notification)
            self.add_notification_widget(widget)

        # also add the blank one at the end
        self.blank = BlankNotificationWidget()
        self.blank.notificationCreated.connect(self.load_notifications)
        self.main_layout.addWidget(self.blank)

    def add_notification_widget(self, widget: NotificationWidget):
        self.widgets.append(widget)
        self.main_layout.addWidget(widget)

    def edit_notification(self, notification: Notification) -> None:
        self.editNotification.emit(notification)
