"""Administrator object to manage data objects and imports, and coordinate operations"""
# todo rewrite function arguments (google style), add type defs

from .hi_objects import BUILD as _BUILD
from typing import Union, List, Dict, Iterable


class Indexer:
    """Actual runner"""

    def __init__(self, allow_duplicates=True):
        """

        """

        self.indexer = _BUILD.new_header_indexer_core()
        """Core services of our header indexing """

        self.fixer = None
        """Fixing services, loaded if header not found"""

        self.allow_duplicates = allow_duplicates
        """Optional setting to allow duplicate header indexes, otherwise will prompt for fix"""

    def run(self, sheet_headers: List[str], head_names: Dict[str, Union[str, Iterable]]):
        """Run HeaderIndexer on given sheet_headers list, using head_names dict to generate a
        new nex dict containing header indexes"""

        # Take headers and head_names, and create ndx_calc
        self.indexer.work.gen_ndx_calc(sheet_headers, head_names)

        # Begin identifying any errors in the parsing
        self.indexer.errors.set()
        self.indexer.check_nonindexed()
        if not self.allow_duplicates:
            self.indexer.check_duplicates()

        print(self.indexer.work.matrix_headers_index_dict)
        input()

        # Prompt to fix
        if self.indexer.errors.error_exists:
            if not self.fixer:
                self.fixer = _BUILD.new_fixer_obj()
            self.fixer.query_fix_nonindexed()

        return self.indexer.work.ndx_calc
