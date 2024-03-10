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
        keyword_optimizer = ApexPlusOptimizer(data=sheet_handler.sponsored_prod_camp,
                                              targets=targets,
                                              presets=presets.ae_presets)
        market_place_filler = "AE_"
    elif MARKET_PLACE == "US":
        keyword_optimizer = ApexPlusOptimizer(data=sheet_handler.sponsored_prod_camp,
                                              targets=targets,
                                              presets=presets.us_presets)
        market_place_filler = "US_"
    else:
        print("[ EROR ] Marketplace is invalid!")
        exit()

    keyword_optimizer.optimize_spa_keywords(exclude_dynamic_bids=False)

    datagram = keyword_optimizer.datasheet

    filename = "Sponsored_Products_Campaigns_" + market_place_filler + str(datetime.datetime.utcnow().date()) + ".xlsx"
    sheet_handler.write_data_file(filename, datagram, "Sponsored Products Campaigns")


if __name__ == "__main__":
    main()
