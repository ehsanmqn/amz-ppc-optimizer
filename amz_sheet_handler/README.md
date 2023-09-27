# Amazon PPC data sheets handler

![GitHub](https://img.shields.io/github/license/ehsanmqn/amz_sheet_handler)
![PyPI](https://img.shields.io/pypi/v/amz_sheet_handler)

**amz_sheet_handler** is a Python package for handling Amazon advertising campaign data efficiently. It provides tools to create, manage, and analyze Amazon Sponsored Products, Sponsored Brands, and Sponsored Display campaigns. With this package, you can automate common tasks related to Amazon advertising campaigns.

## Installation

You can install **amz_sheet_handler** using `pip`:

```bash
pip install amz_sheet_handler
```

## Usage
Here's how you can get started with amz_sheet_handler:

```python
from amz_sheet_handler import AmzSheetHandler

# Initialize the handler with your data file
handler = AmzSheetHandler('your_data_file.xlsx')

# Read data from different sheets
portfolios = handler.read_portfolios()
sponsored_products_campaigns = handler.read_sponsored_products_campaigns()

# Create a new Sponsored Products campaign
new_campaign = AmzSheetHandler.create_spa_campaign("New Campaign")
handler.write_data_file('your_updated_data_file.xlsx', new_campaign, 'NewCampaignSheet')

# And more! Explore the package documentation for detailed usage instructions.
```

## Documentation
For detailed documentation, including examples and API reference, please visit the documentation.

## Contributing
Contributions are welcome! Please follow our contribution guidelines.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
This project was inspired by our need to automate Amazon advertising campaign management.
Thanks to the pandas library for making data manipulation easy.