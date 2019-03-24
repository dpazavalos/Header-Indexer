# todo streamline imports, resort data factories
# todo rewrite function arguments (google style), add type defs

"""HeaderIndexer engine"""

from .hi_objects import BUILD as _BUILD
from typing import Union, List, Dict, Iterable


class HeaderIndexer:
    """Actual runner"""

    def __init__(self, allow_duplicates=True):
        """

        Args:
            allow_duplicates:
        """
        self.indexer = _BUILD.new_header_indexer_core()
        """Core services of our header indexing """

        self.fixer = None
        """Fixing services, loaded if header not found"""

        self.allow_duplicates = allow_duplicates
        """Optional arg to raise issue on any duplicate headers"""

    def _fix_nonindexed(self):
        """In the event a header is not indexed, helper module Fixer is imported and ran. This
        will identify all non-indexed headers and prompt the user to manually select them, or break
        and raise an Error."""
        if not self.fixer:
            self.fixer = _BUILD.new_fixer_obj()

        self.fixer.check_nonindexed()
        self.fixer.check_duplicates()
        self.fixer.query_fix_nonindexed()

    def run(self, sheet_headers: List[str], head_names: Dict[str, Union[str, Iterable]]):
        """Run HeaderIndexer on given sheet_headers list, using head_names dict to generate a
        new nex dict containing header indexes"""

        # Take headers and head_names, and create ndx_calc
        self.indexer.work.gen_ndx_calc(sheet_headers, head_names)

        # Begin identifying any errors in the parsing
        self.indexer.errors.set()

        if None in self.indexer.work.ndx_calc.values():
            # Non Indexed value!
            self._fix_nonindexed()

        return self.indexer.work.ndx_calc
