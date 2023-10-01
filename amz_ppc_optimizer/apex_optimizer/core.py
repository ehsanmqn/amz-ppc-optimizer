USD_TO_AED_FACTOR = 3.67
AED_TO_USD_FACTOR = 0.27

APEX_CLICK_NUM_THRESHOLD = 11
APEX_IMPRESSION_NUM_THRESHOLD = 1000
APEX_TARGET_ACOS_THRESHOLD = 0.3
APEX_HIGH_ACOS = 0.30
APEX_MID_ACOS = 0.25
APEX_LOW_CTR_THRESHOLD = 0.15
APEX_INCREASE_BID_FACTOR = 1.2
APEX_DECREASE_BID_FACTOR = 0.8
APEX_MIN_BID_VALUE = 0.2 * USD_TO_AED_FACTOR
APEX_MAX_BID_VALUE = 2.0 * USD_TO_AED_FACTOR


class ApexOptimizer:
    """
    APEX core
    """

    _data_sheet = None
    _campaigns = []
    _enabled_campaigns = []
    _archived_campaigns = []
    _fixed_bid_campaigns = []
    _dynamic_bidding_campaigns = []

    def __init__(self, data):
        self._data_sheet = data
        self._campaigns = self.get_campaigns()
        self._dynamic_bidding_campaigns = self.get_dynamic_bidding_campaigns()

    @property
    def datasheet(self):
        return self._data_sheet

    def is_dynamic_bidding(self, item):
        return item["Campaign Name (Informational only)"] in self._dynamic_bidding_campaigns

    @staticmethod
    def is_product(item):
        """
        Check whether entity type is a product
        :param item:
        :return:
        """
        return item["Entity"] == "Product Targeting"

    @staticmethod
    def is_keyword(item):
        """
        Check whether entity type is keyword
        :param item:
        :return:
        """
        return item["Entity"] == "Keyword"

    @staticmethod
    def is_keyword_enabled(item):
        """
        Check whether campaign is enabled
        :param item:
        :return:
        """
        return item["State"] == "enabled"

    @staticmethod
    def is_campaign_enabled(item):
        """
        Check whether campaign is enabled
        :param item:
        :return:
        """
        return item["Campaign State (Informational only)"] == "enabled"

    @staticmethod
    def is_ad_group_enabled(item):
        """
        Check whether the Ad group is enabled
        :param item:
        :return:
        """
        return item["Ad Group State (Informational only)"] == "enabled"

    @staticmethod
    def low_click_zero_sale_rule(item):
        """
        Rule 1: Decrease bid for orderless clicked keyword
        :param item:
        :return:
        """
        clicks = int(item["Clicks"])
        orders = int(item["Orders"])

        if clicks >= APEX_CLICK_NUM_THRESHOLD and orders == 0:
            item["Bid"] = APEX_MIN_BID_VALUE
            item["Operation"] = "update"

        return item

    @staticmethod
    def low_impression_low_ctr_low_sale_rule(item):
        """
        Rule 2: Decrease bid for high impressed but low CTR and sales keyword
        :param item:
        :return:
        """
        impression = int(item["Impressions"])
        ctr = float(item["Click-through Rate"])
        orders = int(item["Orders"])

        if impression >= APEX_IMPRESSION_NUM_THRESHOLD and ctr < APEX_LOW_CTR_THRESHOLD and orders == 0:
            item["Bid"] = APEX_MIN_BID_VALUE
            item["Operation"] = "update"

        return item

    @staticmethod
    def profitable_acos_rule(item):
        """
        Rule 3: Increase low ACOS bid
        :param item:
        :return:
        """
        acos = float(item["ACOS"])
        cpc = float(item["CPC"])
        bid = float(item["Bid"])

        if acos != 0 and acos < APEX_TARGET_ACOS_THRESHOLD:
            if cpc > 0:
                item["Bid"] = round(cpc * APEX_INCREASE_BID_FACTOR, 2)
            else:
                item["Bid"] = round(bid * APEX_INCREASE_BID_FACTOR, 2)

            item["Operation"] = "update"

        return item

    @staticmethod
    def unprofitable_acos_rule(item):
        """
        Rule 4: Decrease high ACOS bid
        :param item:
        :return:
        """
        acos = float(item["ACOS"])
        cpc = float(item["CPC"])
        bid = float(item["Bid"])

        if acos != 0 and acos > APEX_TARGET_ACOS_THRESHOLD:
            if cpc > 0:
                item["Bid"] = round((APEX_TARGET_ACOS_THRESHOLD / acos) * cpc, 2)
            else:
                item["Bid"] = round(bid * APEX_INCREASE_BID_FACTOR, 2)

            item["Operation"] = "update"

        return item

    def get_campaigns(self):
        return self._data_sheet[self._data_sheet["Entity"] == "Campaign"]

    def get_dynamic_bidding_campaigns(self):
        return self._data_sheet[
            (self._data_sheet["Entity"] == "Campaign") & (self._data_sheet["Bidding Strategy"] != "Fixed bid")]

    def optimize_spa_keywords(self, exclude_dynamic_bids=True):
        """
        APEX core method
        :return:
        """

        excluded_campaigns = []
        if exclude_dynamic_bids:
            print("[ INFO ] Dynamic bid campaigns excluded from optimization process.")
            excluded_campaigns += self._dynamic_bidding_campaigns["Campaign Name (Informational only)"].values.tolist()

        for index, row in self._data_sheet.iterrows():
            if self.is_keyword(row) or self.is_product(row):
                if self.is_keyword_enabled(row) and \
                        self.is_campaign_enabled(row) and \
                        self.is_ad_group_enabled(row) and \
                        row["Campaign Name (Informational only)"] not in excluded_campaigns:

                    # Optimize keywords' bid
                    # Apply rule 1
                    row = self.low_click_zero_sale_rule(row)
                    if row["Operation"] == "update":
                        self._data_sheet.loc[index] = row
                        continue

                    # Apply rule 2
                    row = self.low_impression_low_ctr_low_sale_rule(row)
                    if row["Operation"] == "update":
                        self._data_sheet.loc[index] = row
                        continue

                    # Apply rule 3
                    row = self.profitable_acos_rule(row)
                    if row["Operation"] == "update":
                        self._data_sheet.loc[index] = row
                        continue

                    # Apply rule 4
                    row = self.unprofitable_acos_rule(row)
                    if row["Operation"] == "update":
                        self._data_sheet.loc[index] = row
