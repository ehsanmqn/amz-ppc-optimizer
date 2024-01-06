APEX_LOW_CTR_THRESHOLD = 0.15

APEX_TARGET_ACOS = 0.3
APEX_INCREASE_BID_BY = 1.2
APEX_DECREASE_BID_BY = 0.9
APEX_MIN_BID_VALUE = 0.2
APEX_MAX_BID_VALUE = 4.0
APEX_HIGH_ACOS_THR = 0.3
APEX_MID_ACOS_THR = 0.25
APEX_CLICK_THR = 11
APEX_IMPRESSION_THR = 1000
APEX_STEP_UP = 0.04


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

    _target_acos_thr = APEX_TARGET_ACOS
    _increase_bid_by = APEX_INCREASE_BID_BY
    _decrease_bid_by = APEX_DECREASE_BID_BY
    _min_bid_value = APEX_MIN_BID_VALUE
    _max_bid_value = APEX_MAX_BID_VALUE
    _high_acos = APEX_HIGH_ACOS_THR
    _mid_acos = APEX_MID_ACOS_THR
    _click_thr = APEX_CLICK_THR
    _impression_thr = APEX_IMPRESSION_THR
    _step_up = APEX_STEP_UP

    def __init__(self, data, desired_acos, change_factor=0.2, min_bid=0.2):
        self._data_sheet = data
        self._campaigns = self.get_campaigns()
        self._dynamic_bidding_campaigns = self.get_dynamic_bidding_campaigns()
        self._target_acos_thr = desired_acos
        self._increase_bid_by = 1 + change_factor
        self._min_bid_value = min_bid

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

    def low_conversion_rate_optimization(self, item):
        """
        Rule 1: Decrease bid for orderless clicked keyword
        :param item:
        :return:
        """
        clicks = int(item["Clicks"])
        orders = int(item["Orders"])

        if clicks >= APEX_CLICK_THR and orders == 0:
            item["Bid"] = self._min_bid_value
            item["Operation"] = "update"

        return item

    def orderless_low_ctr_optimization(self, item):
        """
        Rule 2: Decrease bid for high impressed but low CTR and sales keyword
        :param item:
        :return:
        """
        impression = int(item["Impressions"])
        ctr = float(item["Click-through Rate"])
        orders = int(item["Orders"])

        if impression >= APEX_IMPRESSION_THR and ctr < APEX_LOW_CTR_THRESHOLD and orders == 0:
            item["Bid"] = self._min_bid_value
            item["Operation"] = "update"

        return item

    def profitable_acos_optimization(self, item):
        """
        Rule 3: Increase low ACOS bid
        :param item:
        :return:
        """
        acos = float(item["ACOS"])
        cpc = float(item["CPC"])
        bid = float(item["Bid"])

        if acos != 0 and acos < self._target_acos_thr:
            if cpc > 0:
                item["Bid"] = round(cpc * self._increase_bid_by, 2)
            else:
                item["Bid"] = round(bid * self._increase_bid_by, 2)

            item["Operation"] = "update"

        return item

    def unprofitable_acos_optimization(self, item):
        """
        Rule 4: Decrease high ACOS bid
        :param item:
        :return:
        """
        acos = float(item["ACOS"])
        cpc = float(item["CPC"])
        bid = float(item["Bid"])

        if acos != 0 and acos > self._target_acos_thr:
            if cpc > 0:
                item["Bid"] = round((self._target_acos_thr / acos) * cpc, 2)
            else:
                item["Bid"] = round(bid * self._increase_bid_by, 2)

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
                    row = self.low_conversion_rate_optimization(row)
                    if row["Operation"] == "update":
                        self._data_sheet.loc[index] = row
                        continue

                    # Apply rule 2
                    row = self.orderless_low_ctr_optimization(row)
                    if row["Operation"] == "update":
                        self._data_sheet.loc[index] = row
                        continue

                    # Apply rule 3
                    row = self.profitable_acos_optimization(row)
                    if row["Operation"] == "update":
                        self._data_sheet.loc[index] = row
                        continue

                    # Apply rule 4
                    row = self.unprofitable_acos_optimization(row)
                    if row["Operation"] == "update":
                        self._data_sheet.loc[index] = row

        return self._data_sheet
