class PlacementOptimizer:
    """
    Placement Optimizer
    """

    _data_sheet = None

    # Campaign bidding strategy
    _campaign_bidding_strategies = {
        # We’ll raise your bids (by a maximum of 100%) in real time when your ad may be more likely to convert to a
        # sale, and lower your bids when less likely to convert to a sale.
        "dynamic": "Dynamic bids - up and down",

        # We’ll lower your bids in real time when your ad may be less likely to convert to a sale.
        "dynamic_down": "Dynamic bids - down only",

        # We’ll use your exact bid and any manual adjustments you set, and won’t change your bids based on likelihood
        # of a sale.
        "fixed": "Fixed bid"
    }

    # Adjust bids by placement (replaces Bid+)
    # Example: A AED1.00 bid will remain AED1.00 for placement factor 0%. Dynamic bidding may increase it up to AED2.00.
    _adjust_first_page_factor = 0  # Percentage

    # Example: A AED1.00 bid will remain AED1.00 for placement factor 0%. Dynamic bidding may increase it up to AED1.50.
    _adjust_product_page_factor = 0  # Percentage

    def __init__(self, data):
        self._data_sheet = data

    @property
    def datasheet(self):
        return self._data_sheet

    @staticmethod
    def is_campaign(item):
        """
        Check whether entity type is a campaign
        :param item:
        :return:
        """
        return item["Entity"] == "Campaign"

    @staticmethod
    def is_bidding_adjustment(item):
        """
        Check whether entity type is a Bidding Adjustment
        :param item:
        :return:
        """
        return item["Entity"] == "Bidding Adjustment"

    @staticmethod
    def is_campaign_enabled(item):
        """
        Check whether campaign is enabled
        :param item:
        :return:
        """
        return item["Campaign State (Informational only)"] == "enabled"

    def order_profitable_campaigns(self, order_count=0):
        """
        Return profitable campaigns based on their number of orders
        :return:
        """

        result = self._data_sheet[self._data_sheet["entity"] == "Campaign" and self._data_sheet["Orders"] > order_count]
        result = result.sort_values(by=['Orders'], ascending=False)

        return result

    def adjust_campaign(self, campaigns, strategy, adjust_first_page_factor=None, adjust_product_page_factor=None):
        """
        Bid+ optimizer method
        :return:
        """

        if adjust_first_page_factor is None:
            adjust_first_page_factor = self._adjust_first_page_factor

        if adjust_product_page_factor is None:
            adjust_product_page_factor = self._adjust_product_page_factor

        for index, row in self._data_sheet.iterrows():
            # Adjust campaign
            if self.is_campaign_enabled(row):
                if self.is_campaign(row):
                    if row["Campaign Name (Informational only)"] in campaigns:
                        row["Bidding Strategy"] = self._campaign_bidding_strategies[strategy]
                        row["Operation"] = "update"

                # Adjust bidding adjustment
                if self.is_bidding_adjustment(row):
                    if row["Campaign Name (Informational only)"] in campaigns:
                        if row["Placement"] == "Placement Top":
                            row["Percentage"] = adjust_first_page_factor
                            row["Operation"] = "update"
                        elif row["Placement"] == "Placement Product Page":
                            row["Percentage"] = adjust_product_page_factor
                            row["Operation"] = "update"
