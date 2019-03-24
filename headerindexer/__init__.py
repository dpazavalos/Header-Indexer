# todo Create standalone settings object
# todo streamline imports, resort data factories
# todo rewrite function arguments (google style), add type defs

"""HeaderIndexer engine, with documentation imported from _z_headerindexer_docs"""

from headerindexer.data_factory import Errors, Workings, build as _builder
from typing import List, Dict, Union


class HeaderIndexer:
    """Actual runner"""

    def __init__(self, ):
        """
        HeaderIndexer

        """

        self._errors: Errors = _builder.new_errors_obj()
        """Dataclass for _error_string, _nonindexed, and _duplicates. Resets each run()"""

        self._work: Workings = _builder.new_workings_obj()
        """Dataclass for working data _sheet_headers, _head_names, _ndx_calc. Resets each run()"""

    def _prep_non_persistents(self, sheet_headers, head_names):
        """Clears and sets all public dicts and lists in preparation for a fresh run"""
        self._errors.reset()
        self._work.set(sheet_headers, head_names)

    def _gen_ndx_calc(self):
        """Create a dictionary using head_name keys,
        traducting head_name values into header indexes"""
        # Cross-check reference against corresponding reference's index from sheet_headers_index
        for reference, header in self._work.head_names.items():
            try:
                self._work.ndx_calc[reference] = self._work.sheet_headers_indexes[header]
            except (IndexError, KeyError):
                # Use None to mark missing or bad indexed, and address in later checks
                self._work.ndx_calc[reference] = None

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
        # Checks for any indexes with multiple bound references, via default set dict
        dup_check = {}
        # Create a reverse dict of found index #s, with bound references in a set as values
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
                self._work.sheet_headers_indexes['! Mark as not found !'] = False
                self._work.sheet_headers_indexes["! Leave as 'None'   !"] = None

                for non_indexed in self._errors.nonindexed[::-1]:
                    header = f"Select header for reference: {non_indexed}"
                    chosen_ndx = menu_single.run(self._work.sheet_headers_indexes, header)
                    answer = self._work.sheet_headers_indexes[chosen_ndx]

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
        self._prep_non_persistents(sheet_headers.copy(), head_names.copy())
        self._gen_ndx_calc()
        self._check_nonindexed()
        # self._check_duplicates()
        self._raise_value_error()
        self._query_fix_nonindexed()
        return self._work.ndx_calc

