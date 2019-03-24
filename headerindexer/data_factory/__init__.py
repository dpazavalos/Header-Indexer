"""Accessible aggregate of Data documents and factory object 'build'"""

from headerindexer.data_factory._errors import ErrorsFactory as _ErrorsFactory
# from headerindexer.data_factory._settings import SettingsFactory as _SettingsFactory
from headerindexer.data_factory._workings import WorkingsFactory as _WorkingsFactory


class Errors:
    pass


class Workings:
    pass


class _Factory(_ErrorsFactory, _WorkingsFactory):
    """Factory to build dataclass objects. See build below for use"""


build = _Factory()
"""Importable factory to build dataclass objects"""
