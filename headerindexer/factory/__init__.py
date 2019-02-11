from headerindexer.factory._errors import ErrorsFactory as _ErrorsFactory
from headerindexer.factory._settings import SettingsFactory as _SettingsFactory
from headerindexer.factory._workings import WorkingsFactory as _WorkingsFactory
from headerindexer.factory._z_docs import SettingsDocs as _SettingsDocs, \
    ErrorsDocs as _ErrorsDocs, WorkingsDocs as _WorkingsDocs


class Settings(_SettingsDocs):
    pass


class Errors(_ErrorsDocs):
    pass


class Workings(_WorkingsDocs):
    pass


class _Factory(_SettingsFactory, _ErrorsFactory, _WorkingsFactory):
    """Factory to build dataclass objects. See build below for use"""


build = _Factory()
"""Importable factory to build dataclass objects"""
