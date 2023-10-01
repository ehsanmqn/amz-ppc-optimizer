class PlacementOptimizer:
    """
    Placement core
    Usage:
        placement_optimizer = PlacementOptimizer(loader.sponsored_prod_camp)
        profitable_orders = placement_optimizer.filter_campaigns_acos(threshold=.3)
        print(profitable_orders["Campaign Name"])
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

    def get_campaigns(self):
        return self._data_sheet[self._data_sheet["Entity"] == "Campaign"]

    def filter_campaigns_order(self, threshold=0):
        """
        Return filtered campaigns based on their number of orders
        :return:
        """

        campaigns = self.get_campaigns()
        result = campaigns[campaigns["Orders"] > threshold]
        result = result.sort_values(by=['Orders'], ascending=False)

        return result

    def filter_campaigns_raos(self, threshold=0):
        """
        Return filtered campaigns based on their RAOS
        :return:
        """

        campaigns = self.get_campaigns()
        result = campaigns[campaigns["ROAS"] > threshold]
        result = result.sort_values(by=['ROAS'], ascending=False)

        return result

    def filter_campaigns_name(self, phrase):
        """
        Return filtered campaigns based on their name
        :return:
        """

        campaigns = self.get_campaigns()
        result = campaigns[campaigns["Campaign Name"].str.contains(phrase, na=False)]

        return result

    def filter_campaigns_acos(self, threshold=0):
        """
        Return filtered campaigns based on their ACOS value
        :return:
        """

        campaigns = self.get_campaigns()
        result = campaigns[(campaigns["ACOS"] < threshold) & (campaigns["ACOS"] > 0)]
        result = result.sort_values(by=['ACOS'], ascending=False)

        return result

    def adjust_campaign(self, campaigns, strategy, adjust_first_page_factor=None, adjust_product_page_factor=None):
        """
        Bid+ core method
        :return:
        """

        if adjust_first_page_factor is None:
            adjust_first_page_factor = self._adjust_first_page_factor

        if adjust_product_page_factor is None:
            adjust_product_page_factor = self._adjust_product_page_factor

        if strategy == "fixed":
            adjust_first_page_factor = 0
            adjust_product_page_factor = 0

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
