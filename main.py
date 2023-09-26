import datetime

import pandas

from SheetHandler.sheet_handler import AmzSheetHandler
from Optimizer.apex_optimizer import ApexOptimizer
from Optimizer.search_term_optimizer import SearchTermOptimizer
from Optimizer.placement_optimizer import PlacementOptimizer


EXCLUDE_AD_GROUPS = []


def main():
    sheet_handler = AmzSheetHandler()
    sheet_handler.read_bulk_sheet_report(filename="data.xlsx")
    print(sheet_handler.is_default_exact_campaign_exists(sheet_handler.sponsored_prod_camp))
    return
    # keyword_optimizer = ApexOptimizer(sheet_handler.sponsored_prod_camp)
    # keyword_optimizer.optimize_spa_keywords(exclude_dynamic_bids=True)

    sheet_handler.read_bulk_sheet_report(filename="Sponsored Products Search term report.xlsx")
    search_terms_optimizer = SearchTermOptimizer(sheet_handler.sponsored_product_search_terms)

    # Get profitable and unprofitable search terms based on ACOS value
    profitable_st = search_terms_optimizer.filter_profitable_search_terms(desired_acos=0.3)
    unprofitable_st = search_terms_optimizer.filter_unprofitable_search_terms(desired_acos=0.3)

    # Add profitable search terms to campaigns
    search_terms_optimizer.add_exact_search_terms(profitable_st, 1, "Loofah - Exact - AmzSuggested - 20")
    search_terms_optimizer.add_phrase_search_terms(profitable_st, 1, "Loofah - Phrase - AmzSuggested - 20")
    search_terms_optimizer.add_broad_search_terms(profitable_st, 1, "Loofah - Broad - AmzSuggested - 20")

    # Create campaign example
    camp = sheet_handler.create_spa_campaign("Radium10 - SearchTerms")
    adjustment_top = sheet_handler.create_spa_bidding_adjustment("Radium10 - SearchTerms", placement="Placement Top")
    adjustment_product_page = sheet_handler.create_spa_bidding_adjustment("Radium10 - SearchTerms",
                                                                          placement="Placement Product Page")
    ad_group = sheet_handler.create_spa_ad_group("Radium10 - SearchTerms", "Radium10 - SearchTerms")
    product_ad = sheet_handler.create_spa_product_ad("Radium10 - SearchTerms", "Radium10 - SearchTerms", sku="SI-H77G-MF2F")
    keyword_row = sheet_handler.create_spa_keyword("Radium10 - SearchTerms", "Radium10 - SearchTerms",
                                                   "bath loofah for kids", .73)

    result = [camp, adjustment_top, adjustment_product_page, ad_group, product_ad, keyword_row]

    # filename = "Sponsored Products Campaigns_" + str(datetime.datetime.utcnow().date()) + ".xlsx"
    # campaigns_bulk_sheet.write_data_file(filename, keyword_optimizer.datasheet, "Sponsored Products Campaigns")


if __name__ == "__main__":
    main()
