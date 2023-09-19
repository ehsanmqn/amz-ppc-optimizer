
class PlacementOptimizer:
    """
    Placement Optimizer
    """

    _data_sheet = None

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

    def optimize_campaign(self):
        pass