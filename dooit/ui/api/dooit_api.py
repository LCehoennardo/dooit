from collections.abc import Callable
from typing import TYPE_CHECKING
from textual.message import Message
from dooit.ui.api.plug import PluginManager


if TYPE_CHECKING:
    from ..tui import Dooit


def camel_to_snake(name: str) -> str:
    return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip("_")


class DooitAPI:
    def __init__(self, app: "Dooit") -> None:
        self.app = app
        self.plugin_manager = PluginManager()
        self.plugin_manager.scan()

    def notify(self, message: str) -> None:
        self.app.notify(message)

    def disable_arrow_keys(self):
        pass

    def set_key(self, key: str, callback: Callable) -> None:
        pass

    def handle_key(self, key: str) -> None:
        pass

    def trigger_event(self, event: Message):
        event_name = camel_to_snake(event.__class__.__name__)
        for obj in self.plugin_manager.events[event_name]:
            obj(self)