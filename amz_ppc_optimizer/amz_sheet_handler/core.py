import pandas
import datetime

from amz_ppc_optimizer import settings


class AmzSheetHandler:
    """
    Class for handling Amazon advertising campaign bulk-sheet report data stored in Excel sheets.
    """

    _filename = None
    _portfolios = None
    _sponsored_product_campaigns = None
    _sponsored_brand_campaigns = None
    _sponsored_display_campaigns = None
    _sp_search_term_report = None
    _sponsored_product_search_term_r = None

    def __init__(self, filename=None):
        """
        Initialize the AmzSheetHandler instance.

        :param filename: Path to the Excel file containing campaign data.
        """
        self._filename = filename

    @property
    def portfolios(self):
        """
        Get the DataFrame containing portfolio data.

        :return: A DataFrame containing portfolio data.
        """

        return self._portfolios

    @property
    def sponsored_prod_camp(self):
        """
        Get the DataFrame containing Sponsored Products Campaigns data.

        :return: A DataFrame containing Sponsored Products Campaigns data.
        """

        return self._sponsored_product_campaigns

    @property
    def sponsored_brand_camp(self):
        """
        Get the DataFrame containing Sponsored Brands Campaigns data.

        :return: A DataFrame containing Sponsored Brands Campaigns data.
        """

        return self._sponsored_brand_campaigns

    @property
    def sponsored_disp_camp(self):
        """
        Get the DataFrame containing Sponsored Display Campaigns data.

        :return: A DataFrame containing Sponsored Display Campaigns data.
        """

        return self._sponsored_display_campaigns

    @property
    def sp_search_term_report(self):
        """
        Get the DataFrame containing SP Search Term Report data.

        :return: A DataFrame containing SP Search Term Report data.
        """

        return self._sp_search_term_report

    @property
    def sponsored_product_search_terms(self):
        """
        Get the DataFrame containing sponsored product search term data.

        :return: A DataFrame containing sponsored product search term data.
        """

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
        """
        Filter campaigns in a data sheet based on the 'State' column to include only those that are enabled.

        :param data_sheet: The DataFrame containing campaign data.
        :return: A DataFrame containing only enabled campaigns.
        """

        return data_sheet[(data_sheet["Entity"] == "Campaign") & (data_sheet["State"] == "enabled")]

    @staticmethod
    def filter_paused_campaigns(data_sheet):
        """
        Filter campaigns in a data sheet based on the 'State' column to include only those that are paused.

        :param data_sheet: The DataFrame containing campaign data.
        :return: A DataFrame containing only paused campaigns.
        """

        return data_sheet[(data_sheet["Entity"] == "Campaign") & (data_sheet["State"] == "paused")]

    @staticmethod
    def filter_archived_campaigns(data_sheet):
        """
        Filter campaigns in a data sheet based on the 'State' column to include only those that are archived.

        :param data_sheet: The DataFrame containing campaign data.
        :return: A DataFrame containing only archived campaigns.
        """

        return data_sheet[(data_sheet["Entity"] == "Campaign") & (data_sheet["State"] == "archived")]

    @staticmethod
    def filter_fixed_bid_campaigns(data_sheet):
        """
        Filter campaigns in a data sheet based on the 'Bidding Strategy' column to include only those with a fixed bidding strategy.

        :param data_sheet: The DataFrame containing campaign data.
        :return: A DataFrame containing only campaigns with a fixed bidding strategy.
        """

        return data_sheet[(data_sheet["Entity"] == "Campaign") & (data_sheet["Bidding Strategy"] == "Fixed bid")]

    @staticmethod
    def filter_dynamic_bid_campaigns(data_sheet):
        """
        Filter campaigns in a data sheet based on the 'Bidding Strategy' column to include only those with dynamic bidding strategies.

        :param data_sheet: The DataFrame containing campaign data.
        :return: A DataFrame containing only campaigns with dynamic bidding strategies (excluding 'Fixed bid').
        """

        return data_sheet[(data_sheet["Entity"] == "Campaign") & (data_sheet["Bidding Strategy"] != "Fixed bid")]

    @staticmethod
    def filter_dynamic_up_down_campaigns(data_sheet):
        """
        Filter campaigns in a data sheet based on the 'Bidding Strategy' column to include only those with 'Dynamic bids - up and down'.

        :param data_sheet: The DataFrame containing campaign data.
        :return: A DataFrame containing only campaigns with 'Dynamic bids - up and down' as the bidding strategy.
        """

        return data_sheet[
            (data_sheet["Entity"] == "Campaign") & (data_sheet["Bidding Strategy"] == "Dynamic bids - up and down")]

    @staticmethod
    def filter_dynamic_down_campaigns(data_sheet):
        """
        Filter campaigns in a data sheet based on the 'Bidding Strategy' column to include only those with 'Dynamic bids - down only'.

        :param data_sheet: The DataFrame containing campaign data.
        :return: A DataFrame containing only campaigns with 'Dynamic bids - down only' as the bidding strategy.
        """

        return data_sheet[
            (data_sheet["Entity"] == "Campaign") & (data_sheet["Bidding Strategy"] == "Dynamic bids - down only")]

    @staticmethod
    def filter_exact_match_keywords(data_sheet):
        """
        Filter keywords in a data sheet based on the 'Match Type' column to include only those with 'Exact' match type.

        :param data_sheet: The DataFrame containing keyword data.
        :return: A DataFrame containing only keywords with 'Exact' match type.
        """

        return data_sheet[data_sheet["Match Type"].str.eq("Exact")]

    @staticmethod
    def filter_phrase_match_keywords(data_sheet):
        """
        Filter keywords in a data sheet based on the 'Match Type' column to include only those with 'Phrase' match type.

        :param data_sheet: The DataFrame containing keyword data.
        :return: A DataFrame containing only keywords with 'Phrase' match type.
        """

        return data_sheet[data_sheet["Match Type"].str.eq("Phrase")]

    @staticmethod
    def filter_broad_match_keywords(data_sheet):
        """
        Filter keywords in a data sheet based on the 'Match Type' column to include only those with 'Broad' match type.

        :param data_sheet: The DataFrame containing keyword data.
        :return: A DataFrame
        """

        return data_sheet[data_sheet["Match Type"].str.eq("Broad")]

    @staticmethod
    def get_product_ad_by_campaign(data_sheet, campaign, ad_group):

        return data_sheet[
            (data_sheet["Entity"] == "Product Ad") &
            (data_sheet["Campaign Name (Informational only)"] == campaign) &
            (data_sheet["Ad Group Name (Informational only)"] == ad_group)]

    def read_bulk_sheet_report(self, filename):
        """
        Read data from bulk sheet report Excel file and store it in class variables

        :param filename: Path to the Excel file containing bulk sheet report data
        :return:
        """

        sheet_dataframes = pandas.read_excel(filename, engine="openpyxl", sheet_name=None)
        self._portfolios = sheet_dataframes['Portfolios']
        self._sponsored_product_campaigns = sheet_dataframes['Sponsored Products Campaigns']
        self._sponsored_brand_campaigns = sheet_dataframes['Sponsored Brands Campaigns']
        self._sponsored_display_campaigns = sheet_dataframes['Sponsored Display Campaigns']
        self._sp_search_term_report = sheet_dataframes['SP Search Term Report']

    def read_search_terms_report(self, filename):
        """
        Read the search terms report from an Excel file and store it in the '_sponsored_product_search_term_r' attribute.

        :param filename: The name of the Excel file containing the search terms report.
        :return: A DataFrame containing the search terms report data.
        """

        sheet_dataframes = pandas.read_excel(filename, engine="openpyxl", sheet_name=None)
        self._sponsored_product_search_term_r = sheet_dataframes['Sponsored Product Search Term R']

        return self._sponsored_product_search_term_r

    @staticmethod
    def write_data_file(filename, data, sheet_name):
        """
        Write data to an Excel file with the specified filename and sheet name.

        :param filename: The name of the Excel file to write to.
        :param data: The data (DataFrame) to be written to the file.
        :param sheet_name: The name of the sheet within the Excel file to write the data to.
        """

        data.to_excel(filename, sheet_name=sheet_name, index=False)

    def read_portfolios(self):
        """
        Read portfolio data from an Excel file and store it in the '_portfolios' attribute.

        :return: A DataFrame containing portfolio data.
        """

        self._portfolios = pandas.read_excel(self._filename, sheet_name='Portfolios')
        return self._portfolios

    def read_sponsored_products_campaigns(self):
        """
        Read Sponsored Products campaigns data from an Excel file and store it in the '_sponsored_product_campaigns' attribute.

        :return: A DataFrame containing the Sponsored Products campaigns data.
        """

        self._sponsored_product_campaigns = pandas.read_excel(self._filename, sheet_name='Sponsored Products Campaigns')
        return self._sponsored_product_campaigns

    def read_sponsored_brands_campaigns(self):
        """
        Read Sponsored Brands campaigns data from an Excel file and store it in the '_sponsored_brand_campaigns' attribute.

        :return: A DataFrame containing the Sponsored Brands campaigns data.
        """

        self._sponsored_brand_campaigns = pandas.read_excel(self._filename, sheet_name='Sponsored Brands Campaigns')
        return self._sponsored_brand_campaigns

    def read_sponsored_display_campaigns(self):
        """
        Read Sponsored Display campaigns data from an Excel file and store it in the '_sponsored_display_campaigns' attribute.

        :return: A DataFrame containing the Sponsored Display campaigns data.
        """

        self._sponsored_display_campaigns = pandas.read_excel(self._filename, sheet_name='SP Search Term Report')
        return self._sponsored_display_campaigns

    @staticmethod
    def calculate_statistics(datagram):
        """
        Read Sponsored Product campaigns data and returns statistics.

        :return: avg_acos, avg_raos, avg_conversion_rate, sales, orders, spends, clicks, impressions
        """
        datagram = datagram[datagram['Entity'] == 'Keyword']

        avg_acos = datagram[datagram['ACOS'] > 0].loc[:, 'ACOS'].mean() * 100
        avg_raos = datagram[datagram['ROAS'] > 0].loc[:, 'ROAS'].mean()
        avg_conversion_rate = datagram[datagram['Conversion Rate'] > 0].loc[:, 'Conversion Rate'].mean() * 100
        sales = datagram.loc[:, 'Sales'].sum()
        orders = datagram.loc[:, 'Units'].sum()
        spends = datagram.loc[:, 'Spend'].sum()
        clicks = datagram.loc[:, 'Clicks'].sum()
        impressions = datagram.loc[:, 'Impressions'].sum()

        return avg_acos, avg_raos, avg_conversion_rate, sales, orders, spends, clicks, impressions

    @staticmethod
    def create_spa_campaign(campaign_name, targeting="Manual", budget=10, bidding_strategy="Fixed bid"):
        """
        Create a Sponsored Products campaign along with its related components and return it as a DataFrame.

        :param campaign_name: The name of the campaign.
        :param targeting: The targeting type for the campaign (default is "Manual").
        :param budget: The daily budget for the campaign (default is 10).
        :param bidding_strategy: The bidding strategy for the campaign (default is "Fixed bid").
        :return: A DataFrame containing the created campaign and its related components.
        """

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
        """
        Create a Sponsored Products bidding adjustment along with its related components and return it as a DataFrame.

        :param campaign_name: The name of the campaign where the bidding adjustment should be added.
        :param bidding_strategy: The bidding strategy for the adjustment (default is "Fixed bid").
        :param placement: The placement for the adjustment (default is "Placement Top").
        :param percentage: The percentage value for the adjustment (default is 0).
        :return: A DataFrame containing the created bidding adjustment and its related components.
        """

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
        """
        Create a Sponsored Products ad group along with its related components and return it as a DataFrame.

        :param campaign_name: The name of the campaign where the ad group should be added.
        :param ad_group_name: The name of the ad group.
        :param default_bid: The default bid amount for the ad group (default is 1).
        :return: A DataFrame containing the created ad group and its related components.
        """

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
        """
        Create a Sponsored Products product ad along with its related components and return it as a DataFrame.

        :param campaign_name: The name of the campaign where the product ad should be added.
        :param ad_group_name: The name of the ad group associated with the product ad.
        :param sku: The SKU (Stock Keeping Unit) associated with the product ad (optional).
        :param asin: The ASIN (Amazon Standard Identification Number) associated with the product ad (optional).
        :return: A DataFrame containing the created product ad and its related components.
        """

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
        """
        Create a Sponsored Products keyword along with its related components and return it as a DataFrame.

        :param campaign_name: The name of the campaign where the keyword should be added.
        :param ad_group_name: The name of the ad group associated with the keyword.
        :param keyword: The keyword text.
        :param bid: The bid amount for the keyword.
        :param match_type: The match type of the keyword (default is "Exact").
        :return: A DataFrame containing the created keyword and its related components.
        """

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
    def create_full_spa_campaign(cls, campaign, ad_group):
        """
        Create a full sponsored products campaign along with related components and return it as a DataFrame.

        :param cls: The class itself (AmzSheetHandler).
        :param campaign: The name of the campaign.
        :param ad_group: The name of the ad group associated with the campaign.
        :return: A DataFrame containing the created campaign and its related components.
        """

        camp = cls.create_spa_campaign(campaign)
        adjustment_top = cls.create_spa_bidding_adjustment(campaign, placement="Placement Top")
        adjustment_product_page = cls.create_spa_bidding_adjustment(campaign, placement="Placement Product Page")
        ad_group = cls.create_spa_ad_group(campaign, ad_group)

        frames = [camp, adjustment_top, adjustment_product_page, ad_group]
        result = pandas.concat(frames)

        return result

    @classmethod
    def add_product_ad(cls, datagram, campaign, ad_group, sku, asin=""):
        """
        Add a new product ad and its related components to the provided DataFrame.

        :param cls: The class itself (AmzSheetHandler).
        :param datagram: DataFrame containing campaign data.
        :param campaign: The name of the campaign where the product ad should be added.
        :param ad_group: The name of the ad group associated with the product ad.
        :param sku: The SKU (Stock Keeping Unit) associated with the product ad.
        :param asin: The ASIN (Amazon Standard Identification Number) associated with the product ad.
        :return: A new DataFrame containing the added product ad and related components.
        """

        product_ad = cls.create_spa_product_ad(campaign, ad_group, sku, asin)
        frames = [datagram, product_ad]
        result = pandas.concat(frames)

        return result

    @classmethod
    def add_keyword(cls, datagram, campaign, ad_group, keyword, bid, match_type):
        """
        Add a new keyword and its related components to the provided DataFrame.

        :param cls: The class itself (AmzSheetHandler).
        :param datagram: DataFrame containing campaign data.
        :param campaign: The name of the campaign where the keyword should be added.
        :param ad_group: The name of the ad group associated with the keyword.
        :param keyword: The keyword to be added.
        :param bid: The bid amount for the keyword.
        :param match_type: The match type of the keyword (e.g., "Exact", "Phrase", "Broad").
        :return: A new DataFrame containing the added keyword and related components.
        """

        keyword = cls.create_spa_keyword(campaign, ad_group, keyword, bid, match_type)
        frames = [datagram, keyword]
        result = pandas.concat(frames)

        return result

    @classmethod
    def add_campaign(cls, datagram, campaign, ad_group):
        """
        Add a new campaign and its related components to the provided DataFrame.

        :param cls: The class itself (AmzSheetHandler).
        :param datagram: DataFrame containing campaign data.
        :param campaign: The name of the campaign to be added.
        :param ad_group: The name of the ad group associated with the campaign.
        :return: A new DataFrame containing the added campaign and related components.
        """

        campaign = cls.create_full_spa_campaign(campaign=campaign, ad_group=ad_group)
        frames = [datagram, campaign]
        result = pandas.concat(frames)

        return result

    @staticmethod
    def is_campaign_exists(datagram, campaign_name):
        """
        Check if a campaign with a specific name exists in the provided DataFrame.

        :param datagram: DataFrame containing campaign data.
        :param campaign_name: The name of the campaign to search for.
        :return: True if a campaign with the specified name exists, False otherwise.
        """

        result = datagram[(datagram["Entity"] == "Campaign") & (
                datagram["Campaign Name"] == campaign_name)]

        if len(result) == 0:
            return False
        return True

    @staticmethod
    def is_keyword_exists(datagram, keyword, match_type=None):
        """
        Check if a keyword exists in the provided DataFrame, optionally filtered by match type

        :param datagram: DataFrame containing keyword data.
        :param keyword: The keyword to search for.
        :param match_type: Optional. The match type of the keyword (e.g., "Exact", "Phrase", "Broad").
                          If provided, the search is filtered by this match type.
        :return: True if the keyword (with optional match type) exists, False otherwise.
        """

        if match_type is None:
            result = datagram[(datagram["Entity"] == "Keyword") & (
                    datagram["Keyword Text"] == keyword)]
        else:
            result = datagram[(datagram["Entity"] == "Keyword") & (
                    datagram["Keyword Text"] == keyword) & (datagram["Match Type"] == match_type)]

        if len(result) == 0:
            return False
        return True

    @staticmethod
    def is_product_ad_exists(datagram, campaign, ad_group, sku):

        result = datagram[(datagram["Entity"] == "Product Ad") &
                          (datagram["Campaign Name (Informational only)"] == campaign) &
                          (datagram["Ad Group Name (Informational only)"] == ad_group) &
                          (datagram["SKU"] == sku)]

        if len(result) == 0:
            return False
        return True

    @staticmethod
    def is_default_exact_campaign_exists(datagram):
        """
        Check if the default exact match campaign exists in the provided DataFrame.

        :param datagram: DataFrame containing campaign data.
        :return: True if the default exact match campaign exists, False otherwise.
        """

        result = datagram[(datagram["Entity"] == "Campaign") & (
                datagram["Campaign Name"] == settings.DEFAULT_EXACT_ST_CAMPAIGN_NAME)]

        if len(result) == 0:
            return False
        return True

    @staticmethod
    def is_default_phrase_campaign_exists(datagram):
        """
        Check if the default phrase match campaign exists in the provided DataFrame.

        :param datagram: DataFrame containing campaign data.
        :return: True if the default phrase match campaign exists, False otherwise.
        """

        result = datagram[(datagram["Entity"] == "Campaign") & (
                datagram["Campaign Name"] == settings.DEFAULT_PHRASE_ST_CAMPAIGN_NAME)]

        if len(result) == 0:
            return False
        return True

    @staticmethod
    def is_default_broad_campaign_exists(datagram):
        """
        Check if the default broad match campaign exists in the provided DataFrame.

        :param datagram: DataFrame containing campaign data.
        :return: True if the default broad match campaign exists, False otherwise.
        """
        result = datagram[(datagram["Entity"] == "Campaign") & (
                datagram["Campaign Name"] == settings.DEFAULT_BROAD_ST_CAMPAIGN_NAME)]

        if len(result) == 0:
            return False
        return True
