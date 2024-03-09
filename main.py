import datetime
import presets

from amz_ppc_optimizer import AmzSheetHandler
from amz_ppc_optimizer import ApexOptimizer
from amz_ppc_optimizer import ApexPlusOptimizer

MARKET_PLACE = 'AE'


def main():
    sheet_handler = AmzSheetHandler()
    targets = sheet_handler.read_targets_report("Targets_Mar_9_2024.csv")

    sheet_handler.read_bulk_sheet_report(filename="bulk-aw3emyt3cnq5r-20240120-20240219-1708522968984 (1).xlsx")

    keyword_optimizer = None

    market_place_filler = ''
    if MARKET_PLACE == "AE":
        keyword_optimizer = ApexPlusOptimizer(sheet_handler.sponsored_prod_camp,
                                              targets,
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
                                              excluded_campaigns=presets.ae_excluded_campaigns,
                                              low_impression_max_value=presets.ae_presets["step_up_limit"])
        market_place_filler = "AE_"
    elif MARKET_PLACE == "US":
        keyword_optimizer = ApexPlusOptimizer(sheet_handler.sponsored_prod_camp,
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
                                              excluded_campaigns=presets.us_excluded_campaigns,
                                              low_impression_max_value=presets.us_presets["step_up_limit"])
        market_place_filler = "US_"
    else:
        print("Marketplace is invalid!")
        exit()

    keyword_optimizer.optimize_spa_keywords(exclude_dynamic_bids=False)

    datagram = keyword_optimizer.datasheet

    filename = "Sponsored_Products_Campaigns_" + market_place_filler + str(datetime.datetime.utcnow().date()) + ".xlsx"
    sheet_handler.write_data_file(filename, datagram, "Sponsored Products Campaigns")


if __name__ == "__main__":
    main()
