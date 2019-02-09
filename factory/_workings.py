"""External module of headerIndexer working data. Reset on each run"""

from headerindexer.factory._z_docs import WorkingsDocs, WorkingsFactoryDocs


class Workings(WorkingsDocs):

    def __init__(self, sheet_headers, head_names):
        self.reset(sheet_headers, head_names)

    def reset(self, sheet_headers, head_names):

        self.__setattr__('sheet_headers_indexes',
                         {header: index for index, header in enumerate(sheet_headers)})

        self.__setattr__('head_names', head_names)

        self.ndx_calc.clear()


class WorkingsFactory(WorkingsFactoryDocs):

    @staticmethod
    def _return_workings_obj(sheet_headers, head_names):
        return Workings(sheet_headers, head_names)

    def new_workings_obj(self, sheet_headers, head_names):
        workings_to_return = self._return_workings_obj(sheet_headers, head_names)
        return workings_to_return
