"""Separate module enable to manually select non-indexed headers. The most complex of the lot,
must import header indexer core as super"""

from ._hi_core import HeaderIndexerCore
from .data_obj import DF_BUILD
from typing import Union


class Fixer(HeaderIndexerCore):

    def __init__(self):
        self.errors = DF_BUILD.new_errors_obj()

    def check_nonindexed(self):
        """Checks for any references not found, if self._settings.check_nonindexed = True"""
        for val in self.work.ndx_calc.values():
            if val is None:
                self.errors.nonindexed.append(val)

        # Check to add to _error string
        if self.errors.nonindexed:
            print(self.errors.nonindexed)
            self.add_to_error_string("Non indexed headers!", self.errors.nonindexed)

    def check_duplicates(self):
        """Checks for any duplicate reference ndx, if self._settings.check_duplicates = True"""
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
            self.add_to_error_string("Duplicate header indexes!", self.errors.duplicates)

    def add_to_error_string(self, header, error_arr: Union[dict, list]):
        """Creates error string containing array causing trouble, for stderr out viewing"""
        self.errors.stderr += header + '\n'
        self.errors.stderr += '\n'.join(str(f'    {x}') for x in error_arr.items()) + '\n'

    def raise_value_error(self):
        """Raises ValueError if allowed and needed (Nonindexed values, duplicates)"""
        if self.errors.duplicates or self.errors.nonindexed:
            raise ValueError(self.errors.stderr)

    def query_fix_nonindexed(self):
        """Runs pycolims single menu for non indexed values,
        if self._settings.query_fix = True"""
        if self.errors.nonindexed:

            from headerindexer.hi_objects.pycolims_0_2_0 import Single
            menu_single = Single()
            header = f"{len(self.errors.nonindexed)} non indexed headers. Manually assign?"
            fix_choice = {"Yes": True, 'No, leave their values as None': False}

            if fix_choice[menu_single.run(fix_choice, header)] is True:
                new_nonindexed = []
                self.work.matrix_headers_index_dict['! Mark as not found !'] = False
                self.work.matrix_headers_index_dict["! Leave as 'None'   !"] = None

                for non_indexed in self.errors.nonindexed[::-1]:
                    header = f"Select header for reference: {non_indexed}"
                    chosen_ndx = menu_single.run(self.work.matrix_headers_index_dict, header)
                    answer = self.work.matrix_headers_index_dict[chosen_ndx]

                    if answer is not False:
                        # Add found index, or None, to ndx_calc to return
                        self.work.ndx_calc[non_indexed] = answer
                    elif answer is False:
                        # keep item as not found, return in non-indexed list
                        new_nonindexed = non_indexed
                self.errors.nonindexed = new_nonindexed
