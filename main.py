import datetime

from SheetHandler.sheet_handler import AmzSheetHandler
from Optimizer.apex_optimizer import ApexOptimizer
from Optimizer.search_term_optimizer import SearchTermOptimizer
from Optimizer.placement_optimizer import PlacementOptimizer


EXCLUDE_AD_GROUPS = []


def main():
    sheet_handler = AmzSheetHandler()
    sheet_handler.read_bulk_sheet_report(filename="data.xlsx")

    # keyword_optimizer = ApexOptimizer(sheet_handler.sponsored_prod_camp)
    # keyword_optimizer.optimize_spa_keywords(exclude_dynamic_bids=True)
    print(sheet_handler.sponsored_prod_camp)
    sheet_handler.read_bulk_sheet_report(filename="Sponsored Products Search term report.xlsx")

    search_terms_optimizer = SearchTermOptimizer(sheet_handler.sponsored_product_search_terms)

    # Get profitable and unprofitable search terms based on ACOS value
    profitable_st = search_terms_optimizer.filter_profitable_search_terms(desired_acos=0.3)
    unprofitable_st = search_terms_optimizer.filter_unprofitable_search_terms(desired_acos=0.3)

    # Add profitable search terms to campaigns
    search_terms_optimizer.add_exact_search_terms(profitable_st, 1, "Loofah - Exact - AmzSuggested - 20")
    search_terms_optimizer.add_phrase_search_terms(profitable_st, 1, "Loofah - Phrase - AmzSuggested - 20")
    search_terms_optimizer.add_broad_search_terms(profitable_st, 1, "Loofah - Broad - AmzSuggested - 20")

    # filename = "Sponsored Products Campaigns_" + str(datetime.datetime.utcnow().date()) + ".xlsx"
    # campaigns_bulk_sheet.write_data_file(filename, keyword_optimizer.datasheet, "Sponsored Products Campaigns")


if __name__ == "__main__":
    main()
