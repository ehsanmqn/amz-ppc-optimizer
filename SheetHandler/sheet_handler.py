import pandas
import datetime

import settings


class AmzSheetHandler:
    _filename = None
    _portfolios = None
    _sponsored_product_campaigns = None
    _sponsored_brand_campaigns = None
    _sponsored_display_campaigns = None
    _sp_search_term_report = None
    _sponsored_product_search_term_r = None

    def __init__(self, filename=None):
        self._filename = filename

    @property
    def portfolios(self):
        return self._portfolios

    @property
    def sponsored_prod_camp(self):
        return self._sponsored_product_campaigns

    @property
    def sponsored_brand_camp(self):
        return self._sponsored_brand_campaigns

    @property
    def sponsored_disp_camp(self):
        return self._sponsored_display_campaigns

    @property
    def sp_search_term_report(self):
        return self._sp_search_term_report

    @property
    def sponsored_product_search_terms(self):
        return self._sponsored_product_search_term_r

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

    @staticmethod
    def filter_enabled_campaigns(data_sheet):
        return data_sheet[(data_sheet["Entity"] == "Campaign") & (data_sheet["State"] == "enabled")]

    @staticmethod
    def filter_paused_campaigns(data_sheet):
        return data_sheet[(data_sheet["Entity"] == "Campaign") & (data_sheet["State"] == "paused")]

    @staticmethod
    def filter_archived_campaigns(data_sheet):
        return data_sheet[(data_sheet["Entity"] == "Campaign") & (data_sheet["State"] == "archived")]

    @staticmethod
    def filter_fixed_bid_campaigns(data_sheet):
        return data_sheet[(data_sheet["Entity"] == "Campaign") & (data_sheet["Bidding Strategy"] == "Fixed bid")]

    @staticmethod
    def filter_dynamic_bid_campaigns(data_sheet):
        return data_sheet[(data_sheet["Entity"] == "Campaign") & (data_sheet["Bidding Strategy"] != "Fixed bid")]

    @staticmethod
    def filter_dynamic_up_down_campaigns(data_sheet):
        return data_sheet[
            (data_sheet["Entity"] == "Campaign") & (data_sheet["Bidding Strategy"] == "Dynamic bids - up and down")]

    @staticmethod
    def filter_dynamic_down_campaigns(data_sheet):
        return data_sheet[
            (data_sheet["Entity"] == "Campaign") & (data_sheet["Bidding Strategy"] == "Dynamic bids - down only")]

    @staticmethod
    def filter_exact_match_keywords(data_sheet):
        return data_sheet[data_sheet["Match Type"].str.eq("Exact")]

    @staticmethod
    def filter_phrase_match_keywords(data_sheet):
        return data_sheet[data_sheet["Match Type"].str.eq("Phrase")]

    @staticmethod
    def filter_broad_match_keywords(data_sheet):
        return data_sheet[data_sheet["Match Type"].str.eq("Broad")]

    def read_bulk_sheet_report(self, filename):
        sheet_dataframes = pandas.read_excel(filename, engine="openpyxl", sheet_name=None)
        self._portfolios = sheet_dataframes['Portfolios']
        self._sponsored_product_campaigns = sheet_dataframes['Sponsored Products Campaigns']
        self._sponsored_brand_campaigns = sheet_dataframes['Sponsored Brands Campaigns']
        self._sponsored_display_campaigns = sheet_dataframes['Sponsored Display Campaigns']
        self._sp_search_term_report = sheet_dataframes['SP Search Term Report']

    def read_search_terms_report(self, filename):
        sheet_dataframes = pandas.read_excel(filename, engine="openpyxl", sheet_name=None)
        self._sponsored_product_search_term_r = sheet_dataframes['Sponsored Product Search Term R']

        return self._sponsored_product_search_term_r

    @staticmethod
    def write_data_file(filename, data, sheet_name):
        data.to_excel(filename, sheet_name=sheet_name, index=False)

    def read_portfolios(self):
        self._portfolios = pandas.read_excel(self._filename, sheet_name='Portfolios')
        return self._portfolios

    def read_sponsored_products_campaigns(self):
        self._sponsored_product_campaigns = pandas.read_excel(self._filename, sheet_name='Sponsored Products Campaigns')
        return self._sponsored_product_campaigns

    def read_sponsored_brands_campaigns(self):
        self._sponsored_brand_campaigns = pandas.read_excel(self._filename, sheet_name='Sponsored Brands Campaigns')
        return self._sponsored_brand_campaigns

    def read_sponsored_display_campaigns(self):
        self._sponsored_display_campaigns = pandas.read_excel(self._filename, sheet_name='SP Search Term Report')
        return self._sponsored_display_campaigns

    @staticmethod
    def create_spa_campaign(campaign_name, targeting="Manual", budget=10, bidding_strategy="Fixed bid"):
        # Create a datetime object for the desired date
        date = datetime.datetime.now()

        # Format the date as a string in the "YYYYMMDD" format
        formatted_date = date.strftime("%Y%m%d")

        d = {
            "data": [{
                "Product": "Sponsored Products",
                "Entity": "Campaign",
                "Operation": "Create",
                "Campaign ID": campaign_name,
                "Ad Group ID": "",
                "Portfolio ID": "",
                "Ad ID": "",
                "Keyword ID": "",
                "Product Targeting ID": "",
                "Campaign Name": campaign_name,
                "Ad Group Name": "",
                "Campaign Name (Informational only)": campaign_name,
                "Ad Group Name (Informational only)": "",
                "Portfolio Name (Informational only)": "",
                "Start Date": formatted_date,
                "End Date": "",
                "Targeting Type": targeting,
                "State": "enabled",
                "Campaign State (Informational only)": "",
                "Ad Group State (Informational only)": "",
                "Daily Budget": budget,
                "SKU": "",
                "ASIN (Informational only)": "",
                "Eligibility Status (Informational only)": "",
                "Reason for Ineligibility (Informational only)": "",
                "Ad Group Default Bid": "",
                "Ad Group Default Bid (Informational only)": "",
                "Bid": "",
                "Keyword Text": "",
                "Match Type": "",
                "Bidding Strategy": bidding_strategy,
                "Placement": "",
                "Percentage": "",
                "Product Targeting Expression": "",
                "Resolved Product Targeting Expression (Informational only)": "",
                "Impressions": "",
                "Clicks": "",
                "Click-through Rate": "",
                "Spend": "",
                "Sales": "",
                "Orders": "",
                "Units": "",
                "Conversion Rate": "",
                "ACOS": "",
                "CPC": "",
                "ROAS": ""
            }]
        }

        return pandas.DataFrame(d['data'])

    @staticmethod
    def create_spa_bidding_adjustment(campaign_name, bidding_strategy="Fixed bid", placement="Placement Top",
                                      percentage=0):

        d = {
            "data": [{
                "Product": "Sponsored Products",
                "Entity": "Bidding Adjustment",
                "Operation": "Create",
                "Campaign ID": campaign_name,
                "Ad Group ID": "",
                "Portfolio ID": "",
                "Ad ID": "",
                "Keyword ID": "",
                "Product Targeting ID": "",
                "Campaign Name": "",
                "Ad Group Name": "",
                "Campaign Name (Informational only)": campaign_name,
                "Ad Group Name (Informational only)": "",
                "Portfolio Name (Informational only)": "",
                "Start Date": "",
                "End Date": "",
                "Targeting Type": "",
                "State": "",
                "Campaign State (Informational only)": "",
                "Ad Group State (Informational only)": "",
                "Daily Budget": "",
                "SKU": "",
                "ASIN (Informational only)": "",
                "Eligibility Status (Informational only)": "",
                "Reason for Ineligibility (Informational only)": "",
                "Ad Group Default Bid": "",
                "Ad Group Default Bid (Informational only)": "",
                "Bid": "",
                "Keyword Text": "",
                "Match Type": "",
                "Bidding Strategy": bidding_strategy,
                "Placement": placement,
                "Percentage": percentage,
                "Product Targeting Expression": "",
                "Resolved Product Targeting Expression (Informational only)": "",
                "Impressions": "",
                "Clicks": "",
                "Click-through Rate": "",
                "Spend": "",
                "Sales": "",
                "Orders": "",
                "Units": "",
                "Conversion Rate": "",
                "ACOS": "",
                "CPC": "",
                "ROAS": ""
            }]
        }

        return pandas.DataFrame(d['data'])

    @staticmethod
    def create_spa_ad_group(campaign_name, ad_group_name, default_bid=1):
        d = {
            "data": [{
                "Product": "Sponsored Products",
                "Entity": "Ad Group",
                "Operation": "Create",
                "Campaign ID": campaign_name,
                "Ad Group ID": ad_group_name,
                "Portfolio ID": "",
                "Ad ID": "",
                "Keyword ID": "",
                "Product Targeting ID": "",
                "Campaign Name": "",
                "Ad Group Name": ad_group_name,
                "Campaign Name (Informational only)": campaign_name,
                "Ad Group Name (Informational only)": ad_group_name,
                "Portfolio Name (Informational only)": "",
                "Start Date": "",
                "End Date": "",
                "Targeting Type": "",
                "State": "enabled",
                "Campaign State (Informational only)": "",
                "Ad Group State (Informational only)": "",
                "Daily Budget": "",
                "SKU": "",
                "ASIN (Informational only)": "",
                "Eligibility Status (Informational only)": "",
                "Reason for Ineligibility (Informational only)": "",
                "Ad Group Default Bid": default_bid,
                "Ad Group Default Bid (Informational only)": "",
                "Bid": "",
                "Keyword Text": "",
                "Match Type": "",
                "Bidding Strategy": "",
                "Placement": "",
                "Percentage": "",
                "Product Targeting Expression": "",
                "Resolved Product Targeting Expression (Informational only)": "",
                "Impressions": "",
                "Clicks": "",
                "Click-through Rate": "",
                "Spend": "",
                "Sales": "",
                "Orders": "",
                "Units": "",
                "Conversion Rate": "",
                "ACOS": "",
                "CPC": "",
                "ROAS": ""
            }]
        }

        return pandas.DataFrame(d['data'])

    @staticmethod
    def create_spa_product_ad(campaign_name, ad_group_name, sku="", asin=""):
        d = {
            "data": [{
                "Product": "Sponsored Products",
                "Entity": "Product Ad",
                "Operation": "Create",
                "Campaign ID": campaign_name,
                "Ad Group ID": ad_group_name,
                "Portfolio ID": "",
                "Ad ID": "",
                "Keyword ID": "",
                "Product Targeting ID": "",
                "Campaign Name": "",
                "Ad Group Name": "",
                "Campaign Name (Informational only)": campaign_name,
                "Ad Group Name (Informational only)": ad_group_name,
                "Portfolio Name (Informational only)": "",
                "Start Date": "",
                "End Date": "",
                "Targeting Type": "",
                "State": "enabled",
                "Campaign State (Informational only)": "",
                "Ad Group State (Informational only)": "",
                "Daily Budget": "",
                "SKU": sku,
                "ASIN (Informational only)": asin,
                "Eligibility Status (Informational only)": "",
                "Reason for Ineligibility (Informational only)": "",
                "Ad Group Default Bid": "",
                "Ad Group Default Bid (Informational only)": "",
                "Bid": "",
                "Keyword Text": "",
                "Match Type": "",
                "Bidding Strategy": "",
                "Placement": "",
                "Percentage": "",
                "Product Targeting Expression": "",
                "Resolved Product Targeting Expression (Informational only)": "",
                "Impressions": "",
                "Clicks": "",
                "Click-through Rate": "",
                "Spend": "",
                "Sales": "",
                "Orders": "",
                "Units": "",
                "Conversion Rate": "",
                "ACOS": "",
                "CPC": "",
                "ROAS": ""
            }]
        }

        return pandas.DataFrame(d['data'])

    @staticmethod
    def create_spa_keyword(campaign_name, ad_group_name, keyword, bid, match_type="Exact"):
        d = {
            "data": [{
                "Product": "Sponsored Products",
                "Entity": "Keyword",
                "Operation": "Create",
                "Campaign ID": campaign_name,
                "Ad Group ID": ad_group_name,
                "Portfolio ID": "",
                "Ad ID": "",
                "Keyword ID": "",
                "Product Targeting ID": "",
                "Campaign Name": "",
                "Ad Group Name": "",
                "Campaign Name (Informational only)": campaign_name,
                "Ad Group Name (Informational only)": ad_group_name,
                "Portfolio Name (Informational only)": "",
                "Start Date": "",
                "End Date": "",
                "Targeting Type": "",
                "State": "enabled",
                "Campaign State (Informational only)": "",
                "Ad Group State (Informational only)": "",
                "Daily Budget": "",
                "SKU": "",
                "ASIN (Informational only)": "",
                "Eligibility Status (Informational only)": "",
                "Reason for Ineligibility (Informational only)": "",
                "Ad Group Default Bid": "",
                "Ad Group Default Bid (Informational only)": "",
                "Bid": bid,
                "Keyword Text": keyword,
                "Match Type": match_type,
                "Bidding Strategy": "",
                "Placement": "",
                "Percentage": "",
                "Product Targeting Expression": "",
                "Resolved Product Targeting Expression (Informational only)": "",
                "Impressions": "",
                "Clicks": "",
                "Click-through Rate": "",
                "Spend": "",
                "Sales": "",
                "Orders": "",
                "Units": "",
                "Conversion Rate": "",
                "ACOS": "",
                "CPC": "",
                "ROAS": ""
            }]
        }

        return pandas.DataFrame(d['data'])

    @classmethod
    def create_full_campaign(cls, campaign, ad_group, sku, asin, keyword, bid):
        camp = cls.create_spa_campaign(campaign)
        adjustment_top = cls.create_spa_bidding_adjustment(campaign, placement="Placement Top")
        adjustment_product_page = cls.create_spa_bidding_adjustment(campaign, placement="Placement Product Page")
        ad_group = cls.create_spa_ad_group(campaign, ad_group)
        product_ad = cls.create_spa_product_ad(campaign, ad_group, sku, asin)
        keyword_row = cls.create_spa_keyword(campaign, ad_group, keyword, bid)

        result = [camp, adjustment_top, adjustment_product_page, ad_group, product_ad, keyword_row]

        return result

    @classmethod
    def add_keyword_to_campaign(cls, campaign, ad_group, keyword, bid):
        result = cls.create_spa_keyword(campaign, ad_group, keyword, bid)
        return result

    @staticmethod
    def is_campaign_exists(datagram, campaign_name):
        result = datagram[(datagram["Entity"] == "Campaign") & (
                datagram["Campaign Name"] == campaign_name)]

        if len(result) == 0:
            return False
        return True

    @staticmethod
    def is_default_exact_campaign_exists(datagram):
        result = datagram[(datagram["Entity"] == "Campaign") & (
                datagram["Campaign Name"] == settings.DEFAULT_EXACT_ST_CAMPAIGN_NAME)]

        if len(result) == 0:
            return False
        return True

    @staticmethod
    def is_default_phrase_campaign_exists(datagram):
        result = datagram[(datagram["Entity"] == "Campaign") & (
                datagram["Campaign Name"] == settings.DEFAULT_PHRASE_ST_CAMPAIGN_NAME)]

        if len(result) == 0:
            return False
        return True

    @staticmethod
    def is_default_broad_campaign_exists(datagram):
        result = datagram[(datagram["Entity"] == "Campaign") & (
                datagram["Campaign Name"] == settings.DEFAULT_BROAD_ST_CAMPAIGN_NAME)]

        if len(result) == 0:
            return False
        return True
