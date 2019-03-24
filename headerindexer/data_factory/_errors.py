"""Storage for errors or non-found indexes. Reset on each run"""

from typing import List, Dict


class Errors:
    """Storage for errors or non-found indexes. Includes reset function"""

    stderr: str = ''
    """Error string, to be stderr (dependant on self._settings.raise_error)"""
    nonindexed: List[str] = []
    """Dict of reference headers that were not found in self.sheet_headers"""
    duplicates: Dict[str, int] = []
    """Dict of reference headers that were found more than once"""

    def set(self):
        """Sets all Error holders to default"""
        self.stderr -= self.stderr
        self.nonindexed.clear()
        self.duplicates.clear()


class ErrorsFactory:
    """Factory to generate an Errors object for HeaderIndexer"""

    @staticmethod
    def _return_errors_obj():
        """Return new Errors object"""
        return Errors()

    def new_errors_obj(self):
        """Call to build, init, and return a new errors object"""
        errors_to_return = self._return_errors_obj()
        return errors_to_return
