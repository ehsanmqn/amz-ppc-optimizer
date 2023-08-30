import pandas


class SheetLoader:
    _portfolios = None
    _sponsored_prod_camp = None
    _sponsored_brand_camp = None
    _sponsored_disp_camp = None
    _sp_search_term_report = None

    def __init__(self):
        pass

    @property
    def portfolios(self):
        return self._portfolios

    def read_portfolios(self, filename):
        self._portfolios = pandas.read_excel(filename, sheet_name='Portfolios')
        return self._portfolios

    def read_sponsored_products_campaigns(self, filename):
        self._sponsored_prod_camp = pandas.read_excel(filename, sheet_name='Sponsored Products Campaigns')
        return self._sponsored_prod_camp

    def read_sponsored_brands_campaigns(self, filename):
        self._sponsored_brand_camp = pandas.read_excel(filename, sheet_name='Sponsored Brands Campaigns')
        return self._sponsored_brand_camp

    def read_sponsored_display_campaigns(self, filename):
        self._sponsored_disp_camp = pandas.read_excel(filename, sheet_name='SP Search Term Report')
        return self._sponsored_disp_camp
