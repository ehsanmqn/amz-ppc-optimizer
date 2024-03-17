import pandas

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
NO_DATA_BID_VALUE = 0.31

class ApexPlusOptimizer:
    """
    APEX Plus Optimization Class for optimizing PPC campaigns
    This class try to optimize PPCs based on the APEX algorithm and the Amazon suggested bid. This way prevent the
    optimizer to increase bids more than the suggested bid by amazon in case of over fitted CPCs
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
    _no_data_bid_value = NO_DATA_BID_VALUE
    _excluded_campaigns = []
    _excluded_portfolios = []

    def __init__(self, data, targets,
                 desired_acos=0.3, increase_by=0.2, decrease_by=0.1, max_bid=6, min_bid=0.2, step_up=0.04,
                 high_acos=0.3, mid_acos=0.25, click_limit=11, impression_limit=300, low_impression_max_value=0.35,
                 no_data_bid=0.31, excluded_campaigns=None, excluded_portfolios=None):
        self._data_sheet = data
        self._targets_sheet = targets

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
        self._low_impression_max_value = low_impression_max_value
        self._no_data_bid_value = no_data_bid

        if excluded_portfolios is None:
            self._excluded_portfolios = []

        if excluded_campaigns is None:
            self._excluded_campaigns = []

    def __init__(self, data, targets, presets):

        self._data_sheet = data
        self._targets_sheet = targets
        self._campaigns = handler.get_campaigns(self._data_sheet)
        self._dynamic_bidding_campaigns = handler.get_dynamic_bidding_campaigns(self._data_sheet)
        self._target_acos_thr = presets["desired_acos"]
        self._increase_bid_by = 1 + presets["increase_by"]
        self._decrease_bid_by = 1 - presets["decrease_by"]
        self._max_bid_value = presets["max_bid"]
        self._min_bid_value = presets["min_bid"]
        self._high_acos = presets["high_acos"]
        self._mid_acos = presets["mid_acos"]
        self._click_thr = presets["click_limit"]
        self._impression_thr = presets["impression_limit"]
        self._step_up = presets["step_up"]
        self._low_impression_max_value = presets["low_impression_max_value"]
        self._excluded_campaigns = presets["excluded_campaigns"]
        self._excluded_portfolios = presets["excluded_portfolios"]
        self._no_data_bid_value = presets["no_data_bid"]

    @property
    def datasheet(self):
        return self._data_sheet

    def is_dynamic_bidding(self, item):
        return item["Campaign Name (Informational only)"] in self._dynamic_bidding_campaigns

    def get_suggested_bid(self, item):
        campaign = item["Campaign Name (Informational only)"]
        ad_group = item["Ad Group Name (Informational only)"]

        suggested_bid = 1000
        result = None

        if handler.is_keyword(item):
            keyword = item["Keyword Text"]
            match_type = str(item["Match Type"]).lower()
            result = handler.get_keyword_from_targets(self._targets_sheet, keyword, campaign, ad_group, match_type)

        elif handler.is_product(item):
            asin = item["Product Targeting Expression"]
            result = handler.get_product_from_targets(self._targets_sheet, asin, campaign, ad_group)

        if result is not None:
            # Check for No current data situation
            if pandas.isna(result["Suggested bid"].iloc[0]):
                suggested_bid = self._no_data_bid_value
            else:
                suggested_bid = float(result["Suggested bid"].iloc[0])

        return suggested_bid

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
        suggested_bid = self.get_suggested_bid(item)

        if orders == 0 and impression <= self._impression_thr:
            bid = min(self._low_impression_max_value, min(bid + self._step_up, suggested_bid))

            if bid == suggested_bid:
                bid += 1

            item["Bid"] = bid
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
        suggested_bid = self.get_suggested_bid(item)

        if cpc != 0 and 0 < acos < self._mid_acos:
            bid = min(self._max_bid_value, min(cpc * self._increase_bid_by, suggested_bid))

            if bid == suggested_bid:
                bid += 1

            item["Bid"] = bid
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
        suggested_bid = self.get_suggested_bid(item)

        if cpc != 0 and acos != 0 and acos > self._high_acos:
            item["Bid"] = max(self._min_bid_value, min(self._target_acos_thr / acos * cpc, suggested_bid))
            item["Operation"] = "update"

        return item

    def optimize_spa_keywords(self, exclude_dynamic_bids=True):
        """
        APEX core method
        :return:
        """

        if exclude_dynamic_bids:
            print("[ INFO ] Dynamic bid campaigns excluded from optimization process.")
            dynamic_bid_campaigns = self._dynamic_bidding_campaigns[
                "Campaign Name (Informational only)"].values.tolist()
            self._excluded_campaigns += dynamic_bid_campaigns

        print("[ INFO ] APEX+ Optimizer started.")

        row_counter = 0
        process_counter = 0
        for index, row in self._data_sheet.iterrows():
            row_counter += 1
            if handler.is_keyword_or_product(row):
                if handler.is_enabled(row) and handler.is_campaign_enabled(row) and handler.is_ad_group_enabled(row):

                    if handler.get_portfolio_name(row) in self._excluded_portfolios:
                        continue

                    if handler.get_campaign_name(row) in self._excluded_campaigns:
                        continue

                    # Optimize low conversion rate keywords by decreasing bid
                    row = self.low_conversion_rate_optimization(row)
                    if row["Operation"] == "update":
                        self._data_sheet.loc[index] = row
                        continue

                    # Optimize low impression keywords by stepping up bid
                    row = self.low_impression_optimization(row)
                    if row["Operation"] == "update":
                        self._data_sheet.loc[index] = row
                        continue

                    # Do nothing for low clicked keywords
                    # This can be removed
                    row = self.low_ctr_optimization(row)
                    if row["Operation"] == "update":
                        self._data_sheet.loc[index] = row
                        continue

                    # Increase bid for low ACOS keywords
                    row = self.profitable_acos_optimization(row)
                    if row["Operation"] == "update":
                        self._data_sheet.loc[index] = row
                        continue

                    # Decrease bid for high ACOS keywords
                    row = self.unprofitable_acos_optimization(row)
                    if row["Operation"] == "update":
                        self._data_sheet.loc[index] = row

                    process_counter += 1
                    print("█", end='')

        print("\n\n[ INFO ] {} items out of {} have been processed.".format(process_counter, row_counter))
        print("[ INFO ] Please wait a moment till the process finished.")
        return self._data_sheet
