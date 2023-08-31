from typing import final

from endstone._plugin import PluginBase

from endstone.command import Command, CommandSender
from .plugin_description import PluginDescription


class Plugin(PluginBase):
    def on_load(self) -> None:
        pass

    def on_enable(self) -> None:
        pass

    def on_disable(self) -> None:
        pass

    def on_command(self, sender: CommandSender, command: Command, label: str, *args) -> bool:
        return False

    # noinspection PyAttributeOutsideInit
    @final
    def _init(self, description: PluginDescription) -> None:
        self._description = description

    @property
    def description(self) -> PluginDescription:
        return self._description

    def _get_description(self):
        return self.description
