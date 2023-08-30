import pandas


class SheetLoader:
    _filename = None
    _portfolios = None
    _sponsored_prod_camp = None
    _sponsored_brand_camp = None
    _sponsored_disp_camp = None
    _sp_search_term_report = None

    def __init__(self, filename):
        self._filename = filename

    @property
    def portfolios(self):
        return self._portfolios

    @property
    def sponsored_prod_camp(self):
        return self._sponsored_prod_camp

    @property
    def sponsored_brand_camp(self):
        return self._sponsored_brand_camp

    @property
    def sponsored_disp_camp(self):
        return self._sponsored_disp_camp

    @property
    def sp_search_term_report(self):
        return self._sp_search_term_report

    def read_data_file(self):
        sheet_dataframes = pandas.read_excel(self._filename, sheet_name=None)

        self._portfolios = sheet_dataframes['Portfolios']
        self._sponsored_prod_camp = sheet_dataframes['Sponsored Products Campaigns']
        self._sponsored_brand_camp = sheet_dataframes['Sponsored Brands Campaigns']
        self._sponsored_disp_camp = sheet_dataframes['Sponsored Display Campaigns']
        self._sp_search_term_report = sheet_dataframes['SP Search Term Report']

    def read_portfolios(self):
        self._portfolios = pandas.read_excel(self._filename, sheet_name='Portfolios')
        return self._portfolios

    def read_sponsored_products_campaigns(self):
        self._sponsored_prod_camp = pandas.read_excel(self._filename, sheet_name='Sponsored Products Campaigns')
        return self._sponsored_prod_camp

    def read_sponsored_brands_campaigns(self):
        self._sponsored_brand_camp = pandas.read_excel(self._filename, sheet_name='Sponsored Brands Campaigns')
        return self._sponsored_brand_camp

    def read_sponsored_display_campaigns(self):
        self._sponsored_disp_camp = pandas.read_excel(self._filename, sheet_name='SP Search Term Report')
        return self._sponsored_disp_camp
