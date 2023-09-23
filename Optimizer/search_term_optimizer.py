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

    def find_profitable_search_terms(self):
        pass

    def find_unprofitable_search_terms(self):
        pass

    def add_search_terms(self, exact_match_campaign, phrase_match_campaign, broad_match_campaign):
        pass