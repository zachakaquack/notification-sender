from subprocess import run, DEVNULL, STDOUT
from typing import Any, Dict
from os import walk
from os.path import expanduser, join
from pathlib import Path


class Notification:
    def __init__(
        self,
        app_name: str,
        replaces_id: int,
        app_icon: str | None,
        title: str,
        body: str,
        duration: int,
        index: int | None = None,
    ):
        self.beg = "gdbus call --session \
        --dest org.freedesktop.Notifications \
        --object-path /org/freedesktop/Notifications \
        --method org.freedesktop.Notifications.Notify"
        self.app_name = app_name
        self.replaces_id = f"{replaces_id}"
        self.app_icon = app_icon
        self.title = title
        self.body = body
        self.duration = f"{duration}"
        self.index = index

    def launch_notification(self) -> None:
        resolved_icon = self.get_icon()

        # prefer desktop entry if valid
        if self.app_icon:
            args = f"'[]' '{{\"desktop-entry\": <\"{self.app_icon}\">}}'"
        else:
            args = "'[]' '{}'"

        if resolved_icon:
            icon_arg = resolved_icon
        elif self.app_icon:
            icon_arg = self.app_icon
        else:
            icon_arg = f"{Path.cwd()}/assets/arch.svg"

        full = f"""{self.beg} "{self.app_name}" {self.replaces_id} "{icon_arg}" "{self.title}" "{self.body}" {args} {self.duration}"""

        run(["sh", "-c", full], stdout=DEVNULL, stderr=STDOUT)

    def from_dict(self, d: dict) -> None:
        self.app_name = d["app_name"]
        self.replaces_id = d["replaces_id"]
        self.app_icon = d["app_icon"]
        self.title = d["title"]
        self.body = d["body"]
        self.duration = d["duration"]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "app_name": self.app_name,
            "replaces_id": self.replaces_id,
            "app_icon": self.app_icon,
            "title": self.title,
            "body": self.body,
            "duration": self.duration,
        }

    def get_icon(self) -> str | None:
        """Try to resolve the app_icon into a real file path."""
        if not self.app_icon:
            return None

        icon_dirs = [
            expanduser("~/.local/share/icons"),
            "/usr/share/icons",
            "/usr/share/pixmaps",
        ]

        for base in icon_dirs:
            for root, _, files in walk(base):
                for f in files:
                    if f.startswith(self.app_icon):
                        return join(root, f)

        return None
