
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
    _data = None

    def __init__(self, data):
        self._data = data

    @staticmethod
    def low_click_zero_sale_rule(item):
        clicks = int(item["Clicks"])
        orders = int(item["Orders"])

        if clicks >= APEX_CLICK_NUM_THRESHOLD and orders == 0:
            item["Bid"] = APEX_MIN_BID_VALUE
            item["Operation"] = "update"

            return item
        return None

    @staticmethod
    def low_impression_low_ctr_low_sale_rule(item, impression, ctr, sale, bid):
        pass

    @staticmethod
    def profitable_acos_rule(item, acos, target):
        pass

    @staticmethod
    def unprofitable_acos_rule(item, acos, target):
        pass