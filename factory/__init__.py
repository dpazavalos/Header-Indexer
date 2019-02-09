from headerindexer.factory._errors import ErrorsFactory
from headerindexer.factory._settings import SettingsFactory
from headerindexer.factory._workings import WorkingsFactory
from headerindexer.factory._z_docs import SettingsDocs, ErrorsDocs, WorkingsDocs


class Settings(SettingsDocs):
    pass


class Errors(ErrorsDocs):
    pass


class Workings(WorkingsDocs):
    pass


class _Factory(SettingsFactory, ErrorsFactory, WorkingsFactory):
    """Factory to build dataclass objects. See build below for use"""


build = _Factory()
"""Importable factory to build dataclass objects"""
