import datetime

from SheetHandler.sheet_handler import AmzSheetHandler
from Optimizer.apex_optimizer import ApexOptimizer
from Optimizer.placement_optimizer import PlacementOptimizer


EXCLUDE_AD_GROUPS = []


def main():
    loader = AmzSheetHandler(filename="data.xlsx")
    loader.read_data_file()

    # placement_optimizer = PlacementOptimizer(loader.sponsored_prod_camp)
    # profitable_orders = placement_optimizer.filter_campaigns_acos(threshold=.3)
    # print(profitable_orders["Campaign Name"])

    keyword_optimizer = ApexOptimizer(loader.sponsored_prod_camp)
    keyword_optimizer.optimize_keywords()

    filename = "Sponsored Products Campaigns_" + str(datetime.datetime.utcnow().date()) + ".xlsx"
    loader.write_data_file(filename, keyword_optimizer.datasheet, "Sponsored Products Campaigns")


if __name__ == "__main__":
    main()
