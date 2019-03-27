"""Administrator object to manage data objects and imports, and coordinate operations"""
# todo rewrite function arguments (google style), add type defs

from ._hi_objects import HeaderIndexerEngine
from typing import Union, List, Dict, Iterable


class Indexer:
    """Actual runner"""

    def __init__(self, allow_duplicates=False):
        """

        """

        self.indexer = HeaderIndexerEngine()
        """Core services of our header indexing """

        self.allow_duplicates = allow_duplicates
        """Optional setting to allow duplicate header indexes, otherwise will prompt for fix"""

    def run(self, sheet_headers: List[str], head_names: Dict[str, Union[str, Iterable]]):
        """Run HeaderIndexer on given sheet_headers list, using head_names dict to generate a
        new nex dict containing header indexes"""

        # Take headers and head_names, and create ndx_calc
        self.indexer.work.gen_ndx_calc(sheet_headers, head_names)

        # Begin identifying any errors in the parsing
        self.indexer.check_nonindexed()
        self.indexer.query_fix_nonindexed()

        if not self.allow_duplicates:
            self.indexer.check_duplicates()
            self.indexer.query_fix_duplicates()

        return self.indexer.work.ndx_calc
