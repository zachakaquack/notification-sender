import json
from pathlib import Path

from other.notification_class import Notification
from typing import List, Dict, Any


def get_config_path() -> Path:

    home = Path.home()

    path = Path(f"{home}/.config/fake_notification_caller")

    if not path.exists():
        print("Config path not found")
        path.mkdir(parents=True, exist_ok=True)
        print("~/.config/fake_notification_caller created")

    return path


def get_full_config() -> dict:

    path = get_config_path()
    config_path = f"{path}/config.json"

    if not Path(config_path).exists():
        print("Config not found")
        with open(config_path, "w") as f:
            f.write(f"{json.dumps(write_default_config(), indent=2)}")
            print("Default config created")

    with open(config_path, "r") as f:
        return json.load(f)


def write_default_config() -> dict:

    d = {
        "notifications": [
            {
                "app_name": "vesktop",
                "replaces_id": "9641",
                "app_icon": "vesktop",
                "title": "fake title",
                "body": "fake vesktop notification body",
                "duration": "1000",
            }
        ]
    }

    return d


def notification_decoder(obj: Dict[str, Any]) -> Any:
    if {
        "app_name",
        "replaces_id",
        "app_icon",
        "title",
        "body",
        "duration",
    } <= obj.keys():
        return Notification(
            obj["app_name"],
            obj["replaces_id"],
            obj["app_icon"],
            obj["title"],
            obj["body"],
            obj["duration"],
        )
    return obj


def save_config(config: dict) -> None:
    config_path = get_config_path()
    with open(f"{config_path}/config.json", "w") as f:
        f.write(json.dumps(config, indent=2))


def save_notification(notification: Notification) -> None:
    config = get_full_config()
    config["notifications"].append(notification.to_dict())
    save_config(config)


def create_new_notification() -> Notification:
    n = Notification(
        app_name="Unknown",
        replaces_id=727,
        app_icon=None,
        title="Title",
        body="Body",
        duration=3000,
    )

    save_notification(n)
    return n


def edit_notification(index: int, json_key: str, value: object) -> None:
    config = get_full_config()
    config["notifications"][index][json_key] = value
    save_config(config)


def remove_notification(index: int) -> None:
    config = get_full_config()
    config["notifications"].pop(index)
    save_config(config)


def get_notifications() -> List[Notification]:

    config = get_full_config()
    notifs = []

    for i, notification in enumerate(config["notifications"]):
        n = json.loads(json.dumps(notification), object_hook=notification_decoder)
        n.index = i
        notifs.append(n)

    return notifs
