from .data_obj import DF_BUILD


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

        self.errors = None
        """Dataclass for _error_string, _nonindexed, and _duplicates. Resets each run()"""
