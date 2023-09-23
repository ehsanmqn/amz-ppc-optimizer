import datetime

from SheetHandler.sheet_handler import AmzSheetHandler
from Optimizer.apex_optimizer import ApexOptimizer
from Optimizer.search_term_optimizer import SearchTermOptimizer
from Optimizer.placement_optimizer import PlacementOptimizer


EXCLUDE_AD_GROUPS = []


def main():
    campaigns_bulk_sheet = AmzSheetHandler(filename="data.xlsx")
    campaigns_bulk_sheet.read_data_file(sheet_type="campaigns")

    # placement_optimizer = PlacementOptimizer(loader.sponsored_prod_camp)
    # profitable_orders = placement_optimizer.filter_campaigns_acos(threshold=.3)
    # print(profitable_orders["Campaign Name"])

    # keyword_optimizer = ApexOptimizer(campaigns_bulk_sheet.sponsored_prod_camp)
    # keyword_optimizer.optimize_spa_keywords(exclude_dynamic_bids=True)

    search_terms_sheet = AmzSheetHandler(filename="Sponsored Products Search term report.xlsx")
    search_terms_sheet.read_data_file(sheet_type="terms")

    search_terms_optimizer = SearchTermOptimizer(search_terms_sheet.sponsored_product_search_terms)
    profitable_st = search_terms_optimizer.find_profitable_search_terms(desired_acos=0.3)
    unprofitable_st = search_terms_optimizer.find_unprofitable_search_terms(desired_acos=0.3)
    search_terms_optimizer.add_search_terms(profitable_st, campaigns_bulk_sheet.sponsored_prod_camp, 1, "", "", "")

    # filename = "Sponsored Products Campaigns_" + str(datetime.datetime.utcnow().date()) + ".xlsx"
    # campaigns_bulk_sheet.write_data_file(filename, keyword_optimizer.datasheet, "Sponsored Products Campaigns")


if __name__ == "__main__":
    main()
