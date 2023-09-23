class SearchTermOptimizer:
    """
    Placement Optimizer
    """

    _data_sheet = None

    def __init__(self, data):
        self._data_sheet = data

    @property
    def datasheet(self):
        return self._data_sheet
