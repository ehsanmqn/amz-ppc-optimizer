import datetime
import presets

from amz_ppc_optimizer import AmzSheetHandler
from amz_ppc_optimizer import ApexOptimizer

OPTIMIZE_SEARCH_TERMS = False


def main():
    sheet_handler = AmzSheetHandler()
    sheet_handler.read_bulk_sheet_report(filename="bulk-aw3emyt3cnq5r-20240101-20240118-1705740623578.xlsx")

    keyword_optimizer = ApexOptimizer(sheet_handler.sponsored_prod_camp,
                                      desired_acos=0.3,         # x100 %
                                      increase_by=0.2,          # x100 %
                                      decrease_by=0.1,          # x100 %
                                      max_bid=6,                # Currency
                                      min_bid=0.734,            # Currency
                                      high_acos=0.3,            # x100 %
                                      mid_acos=0.25,            # x100 %
                                      click_limit=11,           # Count
                                      impression_limit=300,     # Count
                                      step_up=0.05,             # Currency
                                      excluded_portfolios=presets.ae_excluded_portfolios,
                                      excluded_campaigns=presets.ae_excluded_campaigns)

    keyword_optimizer.optimize_spa_keywords(exclude_dynamic_bids=False)

    datagram = keyword_optimizer.datasheet

    filename = "Sponsored_Products_Campaigns_" + str(datetime.datetime.utcnow().date()) + ".xlsx"
    sheet_handler.write_data_file(filename, datagram, "Sponsored Products Campaigns")


if __name__ == "__main__":
    main()
