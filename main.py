import datetime
import presets

from amz_ppc_optimizer import AmzSheetHandler
from amz_ppc_optimizer import ApexOptimizer

MARKET_PLACE = 'US'


def main():
    sheet_handler = AmzSheetHandler()
    sheet_handler.read_bulk_sheet_report(filename="bulk-a3xo34lx9b4xu-20240124-20240205-1707312909710.xlsx")

    keyword_optimizer = None

    if MARKET_PLACE == "AE":
        keyword_optimizer = ApexOptimizer(sheet_handler.sponsored_prod_camp,
                                          desired_acos=presets.ae_presets["desired_acos"],
                                          increase_by=presets.ae_presets["increase_by"],
                                          decrease_by=presets.ae_presets["decrease_by"],
                                          max_bid=presets.ae_presets["max_bid"],
                                          min_bid=presets.ae_presets["min_bid"],
                                          high_acos=presets.ae_presets["high_acos"],
                                          mid_acos=presets.ae_presets["mid_acos"],
                                          click_limit=presets.ae_presets["click_limit"],
                                          impression_limit=presets.ae_presets["impression_limit"],
                                          step_up=presets.ae_presets["step_up"],
                                          excluded_portfolios=presets.ae_excluded_portfolios,
                                          excluded_campaigns=presets.ae_excluded_campaigns)
    elif MARKET_PLACE == "US":
        keyword_optimizer = ApexOptimizer(sheet_handler.sponsored_prod_camp,
                                          desired_acos=presets.us_presets["desired_acos"],
                                          increase_by=presets.us_presets["increase_by"],
                                          decrease_by=presets.us_presets["decrease_by"],
                                          max_bid=presets.us_presets["max_bid"],
                                          min_bid=presets.us_presets["min_bid"],
                                          high_acos=presets.us_presets["high_acos"],
                                          mid_acos=presets.us_presets["mid_acos"],
                                          click_limit=presets.us_presets["click_limit"],
                                          impression_limit=presets.us_presets["impression_limit"],
                                          step_up=presets.us_presets["step_up"],
                                          excluded_portfolios=presets.us_excluded_portfolios,
                                          excluded_campaigns=presets.us_excluded_campaigns)

    else:
        print("Marketplace is invalid!")
        exit()

    keyword_optimizer.optimize_spa_keywords(exclude_dynamic_bids=False)

    datagram = keyword_optimizer.datasheet

    filename = "Sponsored_Products_Campaigns_" + str(datetime.datetime.utcnow().date()) + ".xlsx"
    sheet_handler.write_data_file(filename, datagram, "Sponsored Products Campaigns")


if __name__ == "__main__":
    main()
