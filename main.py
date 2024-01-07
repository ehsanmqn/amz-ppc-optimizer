import datetime

from amz_ppc_optimizer import AmzSheetHandler
from amz_ppc_optimizer import ApexOptimizer
from amz_ppc_optimizer import SearchTermOptimizer

OPTIMIZE_SEARCH_TERMS = False

product_portfolio = {
    "Loofah": {
        "search_terms_campaign": "Radium10 - ST",
        "search_terms_campaign_id": "336556679584265",
        "search_terms_ad_group": "Loofah - ST - 30",
        "search_terms_ad_group_id": "411028292540877"
    },
    "Loofah Campaigns": {
        "search_terms_campaign": "Radium10 - ST",
        "search_terms_campaign_id": "336556679584265",
        "search_terms_ad_group": "Loofah - ST - 30",
        "search_terms_ad_group_id": "411028292540877"
    },
    "Hair Brush": {
        "search_terms_campaign": "Radium10 - ST",
        "search_terms_campaign_id": "336556679584265",
        "search_terms_ad_group": "HairBrush - ST - 30",
        "search_terms_ad_group_id": "298971913808937"
    }
}


excluded_campaigns = [
    "Loofah - Long2- Exact - 30",
    "Loofah - Long8 - Exact - 30",
    "Loofah - Long10 - Exact - 30",
    "Loofah - Long3- Exact - 30",
    "Loofah - Long11 - Exact - 30",
    "Loofah - Long1- Exact - 30",
    "Loofah - Long4- Exact - 30",
    "Loofah - Long6- Exact - 30",
    "Loofah - Long7 - Exact - 30",
    "Loofah - Long9 - Exact - 30",
    "Loofah - Long5- Exact - 30",
]

excluded_portfolios = []

def main():
    sheet_handler = AmzSheetHandler()
    sheet_handler.read_bulk_sheet_report(filename="bulk-aw3emyt3cnq5r-20231229-20240104-1704543339045.xlsx")

    keyword_optimizer = ApexOptimizer(sheet_handler.sponsored_prod_camp,
                                      desired_acos=0.3,
                                      increase_by=0.2,
                                      decrease_by=0.1,
                                      max_bid=6,
                                      min_bid=0.734,
                                      high_acos=0.3,
                                      mid_acos=0.25,
                                      click_limit=11,
                                      impression_limit=300,
                                      step_up=0.05)

    keyword_optimizer.optimize_spa_keywords(exclude_dynamic_bids=False)

    datagram = keyword_optimizer.datasheet

    search_termed = ""
    if OPTIMIZE_SEARCH_TERMS is True:
        sheet_handler.read_search_terms_report(filename="Sponsored Products Search term report.xlsx")
        search_terms_optimizer = SearchTermOptimizer(sheet_handler.sponsored_product_search_terms)

        # Get profitable and unprofitable search terms based on ACOS value
        profitable_st = search_terms_optimizer.filter_profitable_search_terms(desired_acos=0.3)
        unprofitable_st = search_terms_optimizer.filter_unprofitable_search_terms(desired_acos=0.3)

        # Add profitable search terms to exact campaigns
        datagram = search_terms_optimizer.add_search_terms(datagram, profitable_st, 1, product_portfolio)
        datagram = search_terms_optimizer.add_search_terms(datagram, unprofitable_st, 0.6, product_portfolio)

        search_termed = "_ST"

    filename = "Sponsored_Products_Campaigns_" + str(datetime.datetime.utcnow().date()) + search_termed + ".xlsx"
    sheet_handler.write_data_file(filename, datagram, "Sponsored Products Campaigns")


if __name__ == "__main__":
    main()
