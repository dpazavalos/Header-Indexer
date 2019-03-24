# todo Create standalone settings object
# todo streamline imports, resort data factories
# todo rewrite function arguments (google style), add type defs

"""HeaderIndexer engine, with documentation imported from _z_headerindexer_docs"""

from headerindexer.data_factory import Errors, Work, build as _builder
from typing import List, Dict, Union


class HeaderIndexer:
    """Actual runner"""

    def __init__(self, ):
        """
        HeaderIndexer

        """

        self._errors: Errors = _builder.new_errors_obj()
        """Dataclass for _error_string, _nonindexed, and _duplicates. Resets each run()"""

        self._work: Work = _builder.new_workings_obj()
        """Dataclass for working data _sheet_headers, _head_names, _ndx_calc. Resets each run()"""

    def _check_nonindexed(self):
        """Checks for any references not found, if self._settings.check_nonindexed = True"""
        for reference in self._work.ndx_calc:
            print(reference, self._work.ndx_calc[reference])
            if self._work.ndx_calc[reference] is None:
                self._errors.nonindexed.append(reference)

        # Check to add to _error string
        if self._errors.nonindexed:
            print(self._errors.nonindexed)
            self._add_to_error_string("Non indexed headers!", self._errors.nonindexed)

    def _check_duplicates(self):
        """Checks for any duplicate reference ndx, if self._settings.check_duplicates = True"""
        # Checks for any indexes with multiple bound references, via default gen_ndx_calc dict
        dup_check = {}
        # Create a reverse dict of found index #s, with bound references in a gen_ndx_calc as values
        for reference, index in self._work.ndx_calc.items():
            dup_check.setdefault(index, set()).add(reference)
        # Check if any indexes correspond to more than one reference
        for index, bound_references in dup_check.items():
            if len(bound_references) > 1:
                for ref in bound_references:
                    self._errors.duplicates[ref] = index

        # Prepare string out to display problem headers
        if self._errors.duplicates:
            self._add_to_error_string("Duplicate header indexes!", self._errors.duplicates)

    def _add_to_error_string(self, header, error_arr: dict):
        """Creates error string containing array causing trouble, for stderr out viewing"""
        self._errors.stderr += header + '\n'
        self._errors.stderr += '\n'.join(str(f'    {x}') for x in error_arr.items()) + '\n'

    def _raise_value_error(self):
        """Raises ValueError if allowed and needed (Nonindexed values, duplicates)"""
        if self._errors.duplicates or self._errors.nonindexed:
            raise ValueError(self._errors.stderr)

    def _query_fix_nonindexed(self):
        """Runs pycolims single menu for non indexed values,
        if self._settings.query_fix = True"""
        if self._errors.nonindexed:

            from headerindexer.pycolims_0_2_0 import Single
            menu_single = Single()
            header = f"{len(self._errors.nonindexed)} non indexed headers. Manually assign?"
            fix_choice = {"Yes": True, 'No, leave their values as None': False}

            if fix_choice[menu_single.run(fix_choice, header)] is True:
                new_nonindexed = []
                self._work.matrix_headers_index_dict['! Mark as not found !'] = False
                self._work.matrix_headers_index_dict["! Leave as 'None'   !"] = None

                for non_indexed in self._errors.nonindexed[::-1]:
                    header = f"Select header for reference: {non_indexed}"
                    chosen_ndx = menu_single.run(self._work.matrix_headers_index_dict, header)
                    answer = self._work.matrix_headers_index_dict[chosen_ndx]

                    if answer is not False:
                        # Add found index, or None, to ndx_calc to return
                        self._work.ndx_calc[non_indexed] = answer
                    elif answer is False:
                        # keep item as not found, return in non-indexed list
                        new_nonindexed = non_indexed
                self._errors.nonindexed = new_nonindexed

    def run(self, sheet_headers, head_names):
        """Run HeaderIndexer on given sheet_headers list, using head_names dict to generate a
        new nex dict containing header indexes"""

        # Take headers and head_names, and create ndx_calc
        self._work.gen_ndx_calc(sheet_headers, head_names)

        # Begin identifying any errors in the parsing
        self._errors.set()
        self._check_nonindexed()

        self._raise_value_error()
        self._query_fix_nonindexed()
        return self._work.ndx_calc

