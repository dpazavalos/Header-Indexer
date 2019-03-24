"""Accessible aggregate of Data documents and factory object 'build'"""


class _Factory:
    """Factory to build dataclass objects. Import build below for use"""

    @staticmethod
    def new_header_indexer_core():
        """Call to build, init, and return a new header indexer core object"""
        from ._hi_core import HeaderIndexerCore
        return HeaderIndexerCore()

    @staticmethod
    def new_fixer_obj():
        from ._fix_issues import Fixer
        return Fixer()


BUILD = _Factory()
"""Importable factory to build dataclass objects"""
