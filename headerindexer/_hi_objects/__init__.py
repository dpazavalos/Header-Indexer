from .data_obj import DF_BUILD
from typing import Union


class HeaderIndexerEngine:
    """
    Central storage for errors and work objects. Incorporated below so HeaderIndexer from above
    can run commands
    """

    def __init__(self):
        """
        Indexer Engine. Contains functions and data objects
        """

        self.work = DF_BUILD.new_work_obj()
        """Primary helper to create and store ndx_calc"""

        self.errors = DF_BUILD.new_errors_obj()
        """Dataclass for _error_string, _nonindexed, and _duplicates. Resets each run()"""

        self.pycolims = None
        """Reference call for pycolims to import to. Assign once needed"""

    # # # Fix Non indexed

    def check_nonindexed(self):
        """Checks for any references not found"""
        for key, val in self.work.ndx_calc.items():
            if val is None:
                self.errors.nonindexed.append(key)

    def query_fix_nonindexed(self):
        """Simple check from user to fix nonindexed headers"""

        print(f'{len(self.errors.nonindexed)} non indexed aliases:\n')
        print('\n'.join(x for x in self.errors.nonindexed))
        print()
        print('Manually assign?')
        print('  (0) Yes')
        print('  (1) No, leave as is (Not recommended!)')
        print('  (2) No, exit script')

        ans = input('> ')
        if ans == '0':
            self._fix_nonindexed()
        elif ans == '2':
            self._raise_value_error()

    def _fix_nonindexed(self):
        """Interactive script to fix non-indexed entries, one by one"""
        for non_indexed in self.errors.nonindexed:
            # for non_indexed in self.errors.nonindexed:
            self._menu_prompt(non_indexed)
        self.errors.nonindexed.clear()

    # # # Fix duplicates

    def check_duplicates(self):
        """Checks for any duplicate reference ndx, if not allow_duplicates"""
        # Checks for any indexes with multiple bound references, via default gen_ndx_calc dict
        dup_check = {}
        # Create a reverse dict of found index #s, with bound references in a gen_ndx_calc as values
        for reference, index in self.work.ndx_calc.items():
            dup_check.setdefault(index, set()).add(reference)

        # Check if any indexes correspond to more than one reference
        for index, bound_aliases in dup_check.items():
            if len(bound_aliases) > 1:
                for ref in bound_aliases:
                    self.errors.duplicates[ref] = index

    def query_fix_duplicates(self):
        """Simple check from user to fix duplicate headers"""
        print(f'{len(self.errors.duplicates)} aliases with duplicate indexes:\n')
        print('\n'.join(f'{key}: {val}' for key, val in self.errors.duplicates.items()))
        print()
        print('Manually assign?')
        print('  (0) Yes')
        print('  (1) No, leave as is (Not recommended!)')
        print('  (2) No, exit script')
        ans = input('> ')
        if ans == '0':
            self._fix_duplicates()
        elif ans == '2':
            self._raise_value_error()

    def _fix_duplicates(self):
        """  """
        for duplicate in self.errors.duplicates:
            self._menu_prompt(duplicate)
        self.errors.duplicates.clear()

        # Check for new/remaining duplicates. Recursively fix
        self.check_duplicates()
        if self.errors.duplicates:
            self.query_fix_duplicates()

    # Depreciate
    def _query_fix_nonindexed(self):
        """Imports and runs pycolims single menu for non indexed or duplicate values"""

        from headerindexer._hi_objects.pycolims_0_2_0 import Single
        menu_single = Single()
        header = f"{len(self.errors.nonindexed)} non indexed headers. Manually assign?"
        fix_choice = {"Yes": True, 'No, exit': False}

        if fix_choice[menu_single.run(fix_choice, header)] is True:
            new_nonindexed = []

            for non_indexed in self.errors.nonindexed[::-1]:
                header = f"Select header for alias: {non_indexed}"
                chosen_ndx = menu_single.run(self.work.matrix_headers_index_dict, header)
                answer = self.work.matrix_headers_index_dict[chosen_ndx]

                self.work.ndx_calc[non_indexed] = answer
            self.errors.nonindexed = new_nonindexed

        else:
            self._raise_value_error()

    # # # Misc tools

    def _menu_prompt(self, alias):
        """Use menu system and matrix_headers_index_dict to have user manually choose a header for
        a given alias. Note that this does not remove the alias from the errors iterable, just
        assigns the index to ndx_calc

        Args:
            alias: Alias for user to manually assign
        """
        # Ensure pycolims single is properly imported
        if not self.pycolims:
            from .pycolims_0_2_0 import Single
            self.pycolims = Single()
        prompt = f"Select header for alias: {alias}"
        # prompt user with a list of all headers, for them to assign the reference to
        chosen_header = self.pycolims.run(self.work.matrix_headers_index_dict, prompt)
        # Get that header's actual column index
        self.work.ndx_calc[alias] = self.work.matrix_headers_index_dict[chosen_header]

    def _raise_value_error(self):
        """Raises ValueError if needed (Nonindexed values, duplicates)"""
        if self.errors.nonindexed:
            self._add_to_error_string("Non indexed headers!", self.errors.nonindexed)
        if self.errors.duplicates:
            self._add_to_error_string("Duplicate header indexes!", self.errors.duplicates)
        if self.errors.error_exists:
            raise IndexError(self.errors.stderr)

    def _add_to_error_string(self, header, error_arr: Union[dict, list]):
        self.errors.stderr += header + '\n'
        self.errors.stderr += '\n'.join(str(f'    {x}') for x in error_arr) + '\n'
