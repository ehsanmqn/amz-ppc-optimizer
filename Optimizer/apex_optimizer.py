USD_TO_AED_FACTOR = 3.67
AED_TO_USD_FACTOR = 0.27

APEX_CLICK_NUM_THRESHOLD = 11
APEX_IMPRESSION_NUM_THRESHOLD = 1000
APEX_TARGET_ACOS_THRESHOLD = 0.3
APEX_LOW_CTR_THRESHOLD = 0.15
APEX_INCREASE_BID_FACTOR = 1.2
APEX_DECREASE_BID_FACTOR = 0.8
APEX_MIN_BID_VALUE = 0.2 * USD_TO_AED_FACTOR
APEX_MAX_BID_VALUE = 2.0 * USD_TO_AED_FACTOR


class ApexOptimizer:
    """
    APEX Optimizer
    """

    _data = None

    def __init__(self, data=None):
        self._data = data

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

    @staticmethod
    def run_apex_optimizer():
        pass
