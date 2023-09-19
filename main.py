import datetime

from SheetHandler.bulk_sheet_handler import AmzBulkSheetHandler
from Optimizer.apex_optimizer import ApexOptimizer
from Optimizer.placement_optimizer import PlacementOptimizer

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

EXCLUDE_AD_GROUPS = []


def is_keyword(item):
    """
    Check whether entity type is keyword
    :param item:
    :return:
    """
    return item["Entity"] == "Keyword"


def is_keyword_enabled(item):
    """
    Check whether campaign is enabled
    :param item:
    :return:
    """
    return item["State"] == "enabled"


def is_campaign_enabled(item):
    """
    Check whether campaign is enabled
    :param item:
    :return:
    """
    return item["Campaign State (Informational only)"] == "enabled"


def is_ad_group_enabled(item):
    """
    Check whether the Ad group is enabled
    :param item:
    :return:
    """
    return item["Ad Group State (Informational only)"] == "enabled"


def main():
    loader = AmzBulkSheetHandler(filename="data.xlsx")
    loader.read_data_file()

    placement_optimizer = PlacementOptimizer(loader.sponsored_prod_camp)
    profitable_orders = placement_optimizer.filter_campaigns_acos(threshold=.3)
    print(profitable_orders)

    # keyword_optimizer = ApexOptimizer(loader.sponsored_prod_camp)
    # keyword_optimizer.optimize_keywords()
    #
    # filename = "Sponsored Products Campaigns_" + str(datetime.datetime.utcnow().date()) + ".xlsx"
    # loader.write_data_file(filename, keyword_optimizer.datasheet, "Sponsored Products Campaigns")


if __name__ == "__main__":
    main()
