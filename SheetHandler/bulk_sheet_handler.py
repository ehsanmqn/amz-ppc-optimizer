import pandas
import openpyxl


class AmzBulkSheetHandler:
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

    @staticmethod
    def is_product(item):
        """
        Check whether entity type is a product
        :param item: Sheet row
        :return: Boolean
        """
        return item["Entity"] == "Product Targeting"

    @staticmethod
    def is_keyword(item):
        """
        Check whether entity type is keyword
        :param item: Sheet row
        :return: Boolean
        """
        return item["Entity"] == "Keyword"

    @staticmethod
    def is_keyword_enabled(item):
        """
        Check whether campaign is enabled
        :param item: Sheet row
        :return: Boolean
        """
        return item["State"] == "enabled"

    @staticmethod
    def is_campaign_enabled(item):
        """
        Check whether campaign is enabled
        :param item: Sheet row
        :return: Boolean
        """
        return item["Campaign State (Informational only)"] == "enabled"

    @staticmethod
    def is_ad_group_enabled(item):
        """
        Check whether the Ad group is enabled
        :param item: Sheet row
        :return: Boolean
        """
        return item["Ad Group State (Informational only)"] == "enabled"

    @staticmethod
    def is_campaign(item):
        """
        Check whether entity type is a campaign
        :param item:
        :return:
        """
        return item["Entity"] == "Campaign"

    @staticmethod
    def is_bidding_adjustment(item):
        """
        Check whether entity type is a Bidding Adjustment
        :param item:
        :return:
        """
        return item["Entity"] == "Bidding Adjustment"

    def read_data_file(self):
        sheet_dataframes = pandas.read_excel(self._filename, engine="openpyxl", sheet_name=None)

        self._portfolios = sheet_dataframes['Portfolios']
        self._sponsored_prod_camp = sheet_dataframes['Sponsored Products Campaigns']
        self._sponsored_brand_camp = sheet_dataframes['Sponsored Brands Campaigns']
        self._sponsored_disp_camp = sheet_dataframes['Sponsored Display Campaigns']
        self._sp_search_term_report = sheet_dataframes['SP Search Term Report']

    @staticmethod
    def write_data_file(filename, data, sheet_name):
        data.to_excel(filename, sheet_name=sheet_name, index=False)

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
