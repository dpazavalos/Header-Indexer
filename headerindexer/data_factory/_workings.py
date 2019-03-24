"""External module of headerIndexer working data. Reset on each run
No init setup, requires startup data passed through reset (Sheet_headers, head_names)"""

from typing import Dict, List


class Workings:
    """External module of headerIndexer working data. Reset on each run
    No init setup, pass startup data passed through set(Sheet_headers, head_names)"""

    def set(self, sheet_headers: List[str], head_names):
        """Sets all working attributes. Requires sheet_headers and head_names"""

        self.sheet_headers_indexes: Dict[str, int] = \
            {header: index for index, header in enumerate(sheet_headers)}
        """Dictionary of all sheet headers as keys and their enumerated index as values"""

        self.head_names = head_names
        """Reference dictionary, to covert to ndx_calc"""

        self.ndx_calc = {}
        """Dictionary to return; converted from self.head_names with values traducted to indexes"""


class WorkingsFactory:
    """Factory to generate a Workings object for HeaderIndexer"""

    @staticmethod
    def _return_workings_obj():
        """Return new Workings object"""
        return Workings()

    def new_workings_obj(self):
        """Call to build, init, and return a new errors object"""
        workings_to_return = self._return_workings_obj()
        return workings_to_return
