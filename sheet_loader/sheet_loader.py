import pandas


class SheetLoader:
    _portfolios = None
    _spcs = None
    _sbcs = None
    _sdcs = None
    _sp_search_term_report = None

    def __init__(self, filename):
        pass

    @property
    def portfolios(self):
        return self._portfolios

    def read_portfolios(self, filename):
        self._portfolios = pandas.read_excel(filename, sheet_name='Portfolios')

    def read_sponsored_products_campaigns(self, filename):
        self._spcs = pandas.read_excel(filename, sheet_name='Sponsored Products Campaigns')