from amz_ppc_optimizer import AmzSheetHandler as handler

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
    APEX Optimization Class for optimizing PPC campaigns
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
    _excluded_campaigns = []
    _excluded_portfolios = []

    def __init__(self, data, desired_acos, increase_by=0.2, decrease_by=0.1, max_bid=6, min_bid=0.2, high_acos=0.3,
                 mid_acos=0.25, click_limit=11, impression_limit=300, step_up=0.04,
                 excluded_campaigns=None, excluded_portfolios=None):

        if excluded_portfolios is None:
            excluded_portfolios = []

        if excluded_campaigns is None:
            excluded_campaigns = []

        self._data_sheet = data
        self._campaigns = handler.get_campaigns(self._data_sheet)
        self._dynamic_bidding_campaigns = handler.get_dynamic_bidding_campaigns(self._data_sheet)

        self._target_acos_thr = desired_acos
        self._increase_bid_by = 1 + increase_by
        self._decrease_bid_by = 1 - decrease_by
        self._max_bid_value = max_bid
        self._min_bid_value = min_bid
        self._high_acos = high_acos
        self._mid_acos = mid_acos
        self._click_thr = click_limit
        self._impression_thr = impression_limit
        self._step_up = step_up

        self._excluded_campaigns = excluded_campaigns
        self._excluded_portfolios = excluded_portfolios

    @property
    def datasheet(self):
        return self._data_sheet

    def is_dynamic_bidding(self, item):
        return item["Campaign Name (Informational only)"] in self._dynamic_bidding_campaigns

    def low_conversion_rate_optimization(self, item):
        """
        Rule 1: Decrease bid for low conversion rate bids
        :param item:
        :return:
        """
        clicks = int(item["Clicks"])
        orders = int(item["Orders"])
        bid = float(item["Bid"])

        if orders == 0 and clicks >= self._click_thr:
            item["Bid"] = max(self._min_bid_value, bid * self._decrease_bid_by)
            item["Operation"] = "update"

        return item

    def low_impression_optimization(self, item):
        """
        Rule 2: Increase bid for low impression bids
        :param item:
        :return:
        """
        impression = int(item["Impressions"])
        orders = int(item["Orders"])
        bid = float(item["Bid"])

        if orders == 0 and impression <= self._impression_thr:
            item["Bid"] = min(self._max_bid_value, bid + self._step_up)
            item["Operation"] = "update"

        return item

    def low_ctr_optimization(self, item):
        """
        Rule 3: Remain bid for low ctr bids
        :param item:
        :return:
        """
        clicks = int(item["Clicks"])
        orders = int(item["Orders"])

        if orders == 0 and clicks < self._click_thr:
            pass

        return item

    def profitable_acos_optimization(self, item):
        """
        Rule 3: Increase low ACOS bid
        :param item:
        :return:
        """
        acos = float(item["ACOS"])
        cpc = float(item["CPC"])

        if cpc != 0 and 0 < acos < self._mid_acos:
            item["Bid"] = min(self._max_bid_value, round(cpc * self._increase_bid_by, 2))
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

        if cpc != 0 and acos != 0 and acos > self._high_acos:
            item["Bid"] = max(self._min_bid_value, round((self._target_acos_thr / acos) * cpc, 2))
            item["Operation"] = "update"

        return item

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
            if handler.is_keyword(row) or handler.is_product(row):
                if handler.is_keyword_enabled(row) and \
                        handler.is_campaign_enabled(row) and \
                        handler.is_ad_group_enabled(row) and \
                        row["Campaign Name (Informational only)"] not in excluded_campaigns:

                    if handler.get_campaign_name(row) in self._excluded_campaigns:
                        continue

                    if handler.get_portfolio_name(row) in self._excluded_portfolios:
                        continue

                    # Optimize keywords' bid
                    # Apply rule 1
                    row = self.low_conversion_rate_optimization(row)
                    if row["Operation"] == "update":
                        self._data_sheet.loc[index] = row
                        continue

                    # Apply rule 2
                    row = self.low_impression_optimization(row)
                    if row["Operation"] == "update":
                        self._data_sheet.loc[index] = row
                        continue

                    # Apply rule 3
                    row = self.low_ctr_optimization(row)
                    if row["Operation"] == "update":
                        self._data_sheet.loc[index] = row
                        continue

                    # Apply rule 4
                    row = self.profitable_acos_optimization(row)
                    if row["Operation"] == "update":
                        self._data_sheet.loc[index] = row
                        continue

                    # Apply rule 5
                    row = self.unprofitable_acos_optimization(row)
                    if row["Operation"] == "update":
                        self._data_sheet.loc[index] = row

        return self._data_sheet
