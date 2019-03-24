"""Accessible aggregate of Data documents and factory object 'build'"""
from . import _errors, _workings


class Errors(_errors.Errors):
    pass


class Work(_workings.Work):
    pass


class _Factory(_errors.ErrorsFactory, _workings.WorkingsFactory):
    """Factory to build dataclass objects. See build below for use"""


build = _Factory()
"""Importable factory to build dataclass objects"""
