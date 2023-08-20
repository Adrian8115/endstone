import importlib.util
import io
import sys
import zipimport
from importlib.machinery import ModuleSpec
from pathlib import Path
from types import ModuleType

from endstone._plugin import IPluginLoader

from .plugin import Plugin
from .plugin_description import PluginDescriptionFile

__all__ = ["ZipPluginLoader", "SourcePluginLoader"]


class PluginLoader(IPluginLoader):
    _file_filters = []

    def __init__(self):
        IPluginLoader.__init__(self)

    def enable_plugin(self, plugin: Plugin) -> None:
        if not plugin.is_enabled():
            plugin.logger.info(f"Enabling {plugin.get_description().get_fullname()}")
            # noinspection PyProtectedMember
            plugin._set_enabled(True)

    def disable_plugin(self, plugin: Plugin) -> None:
        if plugin.is_enabled():
            plugin.logger.info(f"Disabling {plugin.get_description().get_fullname()}")
            # noinspection PyProtectedMember
            plugin._set_enabled(False)

    def get_plugin_filters(self) -> list[str]:
        return self._file_filters.copy()


class ZipPluginLoader(PluginLoader):
    _file_filters = [r"\.whl$", r"\.zip$"]

    def load_plugin(self, file: str) -> Plugin:
        assert file is not None, "File cannot be None"

        importer = zipimport.zipimporter(file)

        try:
            # noinspection PyTypeChecker
            fp = io.BytesIO(importer.get_data("plugin.toml"))
            description = PluginDescriptionFile(fp)

        except Exception as e:
            raise RuntimeError(f"Unable to load 'plugin.toml': {e}")

        try:
            main = description.get_main()
            parts = main.split(".")
            class_name = parts.pop()
            module_name = ".".join(parts)

            module = importer.load_module(module_name)
            plugin = getattr(module, class_name)()
            assert isinstance(plugin, Plugin), f"Main class {main} does not extend endstone.plugin.Plugin"

            # noinspection PyProtectedMember
            plugin._init(description)
            return plugin
        except Exception as e:
            raise RuntimeError(f"Unable to load plugin {description.get_fullname()}: {e}")


class SourcePluginLoader(PluginLoader):
    _file_filters = [r"plugin\.toml$"]

    def load_plugin(self, file: str) -> Plugin:
        assert file is not None, "File cannot be None"
        file = Path(file)
        dir_name = file.resolve().parent

        try:
            with open(file, "rb") as f:
                description = PluginDescriptionFile(f)

        except Exception as e:
            raise RuntimeError(f"Unable to load 'plugin.toml': {e}")

        try:
            main = description.get_main()
            parts = main.split(".")
            class_name = parts.pop()
            module_name = ".".join(parts)

            spec = self._get_module_spec(module_name, dir_name)
            if not spec:
                raise ModuleNotFoundError(module_name)

            module = self._load_module_from_spec(spec)
            plugin = getattr(module, class_name)()
            assert isinstance(plugin, Plugin), f"Main class {main} does not extend endstone.plugin.Plugin"

            # noinspection PyProtectedMember
            plugin._init(description)
            return plugin

        except Exception as e:
            raise RuntimeError(f"Unable to load plugin {description.get_fullname()}: {e}")

    @staticmethod
    def _load_module_from_spec(spec: ModuleSpec) -> ModuleType:
        if spec.name in sys.modules:
            return sys.modules[spec.name]
        else:
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            return module

    @staticmethod
    def _get_module_spec(module_name: str, path: Path) -> ModuleSpec:
        module_parts = module_name.split(".")

        # Check for package
        package_location = path.joinpath(*module_parts, "__init__.py")
        if package_location.exists():
            return importlib.util.spec_from_file_location(module_name, package_location)

        # Check for module file
        module_file = module_parts.pop() + ".py"
        module_location = path.joinpath(*module_parts, module_file)
        if module_location.exists():
            return importlib.util.spec_from_file_location(module_name, module_location)

        raise ModuleNotFoundError(module_name)