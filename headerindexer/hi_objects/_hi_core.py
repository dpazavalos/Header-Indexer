from .data_obj import DF_BUILD
from typing import Union


class HeaderIndexerCore:
    """
    Central storage for errors and work objects. Incorporated below so HeaderIndexer from above
    can run commands
    """

    def __init__(self):
        """
        HeaderIndexer

        """

        self.work = DF_BUILD.new_work_obj()
        """Primary helper to create and store ndx_calc"""

        self.errors = DF_BUILD.new_errors_obj()
        """Dataclass for _error_string, _nonindexed, and _duplicates. Resets each run()"""

    def check_nonindexed(self):
        """Checks for any references not found"""
        for key, val in self.work.ndx_calc.items():
            if val is None:
                self.errors.nonindexed.append(key)

        if self.errors.error_exists:
            self.errors.stderr += "Non indexed headers!"
            self.errors.stderr += '\n'.join(str(f'    {x}') for x in self.errors.nonindexed)

    '''def check_duplicates(self):
        """Checks for any duplicate reference ndx, if not allow_duplicates"""
        # Checks for any indexes with multiple bound references, via default gen_ndx_calc dict
        dup_check = {}
        # Create a reverse dict of found index #s, with bound references in a gen_ndx_calc as values
        for reference, index in self.work.ndx_calc.items():
            dup_check.setdefault(index, set()).add(reference)

        # Check if any indexes correspond to more than one reference
        for index, bound_references in dup_check.items():
            if len(bound_references) > 1:
                for ref in bound_references:
                    self.errors.duplicates[ref] = index

        # Prepare string out to display problem headers
        if self.errors.duplicates:
            self.add_to_error_string("Duplicate header indexes!", self.errors.duplicates)'''

    def add_to_error_string(self, header, error_arr: Union[dict, list]):
        """Creates error string containing array causing trouble, for stderr out viewing"""

