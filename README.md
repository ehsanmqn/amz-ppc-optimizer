# Amazon PPC Optimizer

This project is a Python script that optimizes Amazon PPC campaigns by analyzing search term reports and adjusting campaign keywords and bids to improve advertising performance.

## Requirements

Before running the script, make sure you have the following prerequisites installed:

- Python 3.x
- Required Python packages (specified in `requirements.txt`)

You can install the required packages by running:

```bash
pip install amz-ppc-optimizer
```

## Usage
Data Preparation
- Bulk sheet report containing campaign data
- Search term report for sponsored products

Sample usage
```python
    sheet_handler = AmzSheetHandler()
    sheet_handler.read_bulk_sheet_report(filename="amz-ppc-bulk-file-name.xlsx")

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
```

### Optimization Process
The script reads the campaign data from data.xlsx and optimizes keywords in sponsored product campaigns.
It also reads the search term report from Sponsored Products Search term report.xlsx.
Profitable and unprofitable search terms are determined based on the specified ACOS (Advertising Cost of Sales) threshold.
Profitable search terms are added to exact match campaigns, and bids are adjusted.
Unprofitable search terms are added with reduced bids to maintain visibility but control costs.


## Configuration
You can configure the optimization settings in the script:

Adjust the desired_acos value to set your desired ACOS threshold for filtering profitable and unprofitable search terms.

## License
This project is licensed under the MIT License - see the LICENSE file for details.