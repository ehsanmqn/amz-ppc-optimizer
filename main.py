import datetime

import pandas

import settings
from SheetHandler.sheet_handler import AmzSheetHandler
from Optimizer.apex_optimizer import ApexOptimizer
from Optimizer.search_term_optimizer import SearchTermOptimizer
from Optimizer.placement_optimizer import PlacementOptimizer

EXCLUDE_AD_GROUPS = []


def add_search_terms(datagram, search_terms, bid_factor):
    # Add profitable search terms to exact campaigns
    exact_camp_name = settings.DEFAULT_EXACT_ST_CAMPAIGN_NAME
    if AmzSheetHandler.is_campaign_exists(datagram, exact_camp_name) is False:
        datagram = AmzSheetHandler.add_campaign(datagram, exact_camp_name, exact_camp_name)

    # Add profitable search terms to phrase campaigns
    phrase_camp_name = settings.DEFAULT_PHRASE_ST_CAMPAIGN_NAME
    if AmzSheetHandler.is_campaign_exists(datagram, phrase_camp_name) is False:
        datagram = AmzSheetHandler.add_campaign(datagram, phrase_camp_name, phrase_camp_name)

    # Add profitable search terms to broad campaigns
    broad_camp_name = settings.DEFAULT_BROAD_ST_CAMPAIGN_NAME
    if AmzSheetHandler.is_campaign_exists(datagram, broad_camp_name) is False:
        datagram = AmzSheetHandler.add_campaign(datagram, broad_camp_name, broad_camp_name)

    for index, row in search_terms.iterrows():
        keyword = row["Customer Search Term"]
        if AmzSheetHandler.is_keyword_exists(datagram, keyword, "Exact") is False:
            bid = float(row["Cost Per Click (CPC)"])
            datagram = AmzSheetHandler.add_keyword(datagram, exact_camp_name, exact_camp_name, keyword, bid * bid_factor, "Exact")
            datagram = AmzSheetHandler.add_keyword(datagram, phrase_camp_name, phrase_camp_name, keyword, bid * bid_factor, "Phrase")
            datagram = AmzSheetHandler.add_keyword(datagram, broad_camp_name, broad_camp_name, keyword, bid * bid_factor, "Broad")
            print("##### {} added".format(keyword))
        else:
            print(">>>>> {} exists".format(keyword))
    return datagram


def main():
    sheet_handler = AmzSheetHandler()
    sheet_handler.read_bulk_sheet_report(filename="bulk-aw3emyt3cnq5r-20230828-20230829-1693310953861.xlsx")

    keyword_optimizer = ApexOptimizer(sheet_handler.sponsored_prod_camp)
    keyword_optimizer.optimize_spa_keywords(exclude_dynamic_bids=True)

    sheet_handler.read_search_terms_report(filename="Sponsored Products Search term report.xlsx")
    search_terms_optimizer = SearchTermOptimizer(sheet_handler.sponsored_product_search_terms)

    # Get profitable and unprofitable search terms based on ACOS value
    profitable_st = search_terms_optimizer.filter_profitable_search_terms(desired_acos=0.3)
    unprofitable_st = search_terms_optimizer.filter_unprofitable_search_terms(desired_acos=0.3)

    # Add profitable search terms to exact campaigns
    datagram = keyword_optimizer.datasheet
    datagram = add_search_terms(datagram, profitable_st, 1)
    datagram = add_search_terms(datagram, unprofitable_st, 0.6)

    filename = "Sponsored Products Campaigns_" + str(datetime.datetime.utcnow().date()) + ".xlsx"
    sheet_handler.write_data_file(filename, datagram, "Sponsored Products Campaigns")


if __name__ == "__main__":
    main()
