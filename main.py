import datetime

from amz_ppc_optimizer import AmzSheetHandler
from amz_ppc_optimizer import ApexOptimizer
from amz_ppc_optimizer import SearchTermOptimizer

optimize_search_terms = False


def main():
    sheet_handler = AmzSheetHandler()
    sheet_handler.read_bulk_sheet_report(filename="bulk-aw3emyt3cnq5r-20230818-20231015-1697524149157.xlsx")

    keyword_optimizer = ApexOptimizer(sheet_handler.sponsored_prod_camp, desired_acos=0.3, min_bid=0.734)
    keyword_optimizer.optimize_spa_keywords(exclude_dynamic_bids=False)

    datagram = keyword_optimizer.datasheet

    search_termed = ""
    if optimize_search_terms is True:
        sheet_handler.read_search_terms_report(filename="Sponsored Products Search term report.xlsx")
        search_terms_optimizer = SearchTermOptimizer(sheet_handler.sponsored_product_search_terms)

        # Get profitable and unprofitable search terms based on ACOS value
        profitable_st = search_terms_optimizer.filter_profitable_search_terms(desired_acos=0.3)
        unprofitable_st = search_terms_optimizer.filter_unprofitable_search_terms(desired_acos=0.3)

        # Add profitable search terms to exact campaigns
        datagram = search_terms_optimizer.add_search_terms(datagram, profitable_st, 1)
        datagram = search_terms_optimizer.add_search_terms(datagram, unprofitable_st, 0.6)

        search_termed = "ST_"

    filename = "Sponsored_Products_Campaigns_" + search_termed + str(datetime.datetime.utcnow().date()) + ".xlsx"
    sheet_handler.write_data_file(filename, datagram, "Sponsored Products Campaigns")


if __name__ == "__main__":
    main()
