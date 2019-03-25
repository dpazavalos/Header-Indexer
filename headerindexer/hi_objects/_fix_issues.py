"""Separate module enable to manually select non-indexed headers. Kept separate to manage pycolims
import, and is only loaded if there are errors"""

from ._hi_core import HeaderIndexerCore


class Fixer(HeaderIndexerCore):

    # def __init__(self):
    #    super().__init__()

    def raise_value_error(self):
        """Raises ValueError if needed (Nonindexed values, duplicates)"""
        if self.errors.duplicates or self.errors.nonindexed:
            raise ValueError(self.errors.stderr)

    def query_fix_nonindexed(self):
        """Runs pycolims single menu for non indexed or duplicate values"""

        from headerindexer.hi_objects.pycolims_0_2_0 import Single
        menu_single = Single()
        header = f"{len(self.errors.nonindexed)} non indexed headers. Manually assign?"
        fix_choice = {"Yes": True, 'No, exit': False}

        if fix_choice[menu_single.run(fix_choice, header)] is True:
            new_nonindexed = []
            print(self.errors.nonindexed)
            print(self.work.matrix_headers_index_dict)
            input()

            for non_indexed in self.errors.nonindexed[::-1]:
                header = f"Select header for alias: {non_indexed}"
                chosen_ndx = menu_single.run(self.work.matrix_headers_index_dict.keys(), header)
                answer = self.work.matrix_headers_index_dict[chosen_ndx]

                self.work.ndx_calc[non_indexed] = answer
            self.errors.nonindexed = new_nonindexed

        else:
            self.raise_value_error()
