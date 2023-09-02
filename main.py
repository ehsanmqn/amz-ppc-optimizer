import datetime

from sheet_loader.loader import SheetLoader
from optimizer.ppc_optimizer import PpcOptimizer

CLICK_NUM_THRESHOLD = 11
IMPRESSION_NUM_THRESHOLD = 1000
TARGET_ACOS_THRESHOLD = 0.3
LOW_CTR_THRESHOLD = 0.15
INCREASE_RATIO = 1.2
DECREASE_RATIO = 0.8
MIN_BID_VALUE = 0.73  # AED
MAX_BID_VALUE = 6.0  # AED

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
    loader = SheetLoader(filename="data.xlsx")
    loader.read_data_file()
    spc = loader.sponsored_prod_camp

    for index, row in spc.iterrows():
        # Optimize keywords' bid
        if is_keyword(row) and \
                is_keyword_enabled(row) and \
                is_campaign_enabled(row) and \
                is_ad_group_enabled(row):

            is_bid_updated = False
            update_rules = []

            keyword_bid = float(row["Bid"])
            keyword_acos = float(row["ACOS"])
            keyword_impressions = int(row["Impressions"])
            keyword_clicks = int(row["Clicks"])
            keyword_spend = float(row["Clicks"])
            keyword_roas = float(row["ROAS"])
            keyword_orders = int(row["Orders"])
            keyword_sales = float(row["Sales"])
            keyword_ctr = float(row["Click-through Rate"])
            keyword_average_cpc = float(row["CPC"])

            # Rule 1: Decrease bid for orderless clicked keyword
            if keyword_clicks >= CLICK_NUM_THRESHOLD and keyword_orders == 0:
                row["Bid"] = MIN_BID_VALUE

                is_bid_updated = True
                update_rules.append("Rule 1")

            # Rule 2: Decrease bid for high impressed but low CTR and sales keyword
            if keyword_impressions >= IMPRESSION_NUM_THRESHOLD and \
                    keyword_ctr < LOW_CTR_THRESHOLD and \
                    keyword_orders == 0:
                row["Bid"] = MIN_BID_VALUE

                is_bid_updated = True
                update_rules.append("Rule 2")

            # Rule 3: Increase low ACOS bid
            if keyword_acos != 0 and keyword_acos < TARGET_ACOS_THRESHOLD:
                if keyword_average_cpc > 0:
                    row["Bid"] = round(keyword_average_cpc * INCREASE_RATIO, 2)
                else:
                    row["Bid"] = round(keyword_bid * INCREASE_RATIO, 2)

                is_bid_updated = True
                update_rules.append("Rule 3 ACOS: {}".format(keyword_acos))

            # Rule 4: Decrease high ACOS bid
            if keyword_acos > TARGET_ACOS_THRESHOLD:
                row["Bid"] = round((TARGET_ACOS_THRESHOLD / keyword_acos) * keyword_average_cpc, 2)

                is_bid_updated = True
                update_rules.append("Rule 4 ACOS: {}".format(keyword_acos))

            if is_bid_updated:
                row["Operation"] = "update"
                spc.loc[index] = row
                print(index, row["Keyword Text"], keyword_bid, row["Bid"], update_rules)

    filename = "Sponsored Products Campaigns_" + str(datetime.datetime.utcnow().date()) + ".xlsx"
    loader.write_data_file(filename, spc, "Sponsored Products Campaigns")


if __name__ == "__main__":
    main()
