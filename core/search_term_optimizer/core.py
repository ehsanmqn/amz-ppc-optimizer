

class SearchTermOptimizer:
    """
    Placement core
    """

    _data_sheet = None

    def __init__(self, data):
        self._data_sheet = data

    @property
    def datasheet(self):
        return self._data_sheet

    def create_exact_keyword(self, campaign_name):
        pass

    def filter_profitable_search_terms(self, desired_acos):
        """
        Return search terms that have ACOS lower than desired ACOS
        :return:
        """

        search_terms = self._data_sheet[self._data_sheet["Match Type"].isin(["EXACT", "PHRASE", "BROAD"])]
        result = search_terms[(search_terms["Total Advertising Cost of Sales (ACOS) "] < desired_acos) & (
                search_terms["Total Advertising Cost of Sales (ACOS) "] > 0)]
        result = result.sort_values(by=["Total Advertising Cost of Sales (ACOS) "], ascending=False)

        return result

    def filter_unprofitable_search_terms(self, desired_acos):
        """
        Return search terms that have ACOS higher than desired ACOS
        :param desired_acos:
        :return:
        """

        search_terms = self._data_sheet[self._data_sheet["Match Type"].isin(["EXACT", "PHRASE", "BROAD"])]
        result = search_terms[(search_terms["Total Advertising Cost of Sales (ACOS) "] > desired_acos)]
        result = result.sort_values(by=["Total Advertising Cost of Sales (ACOS) "], ascending=False)

        return result

        pass

    @staticmethod
    def add_exact_search_terms(search_terms, impact_factor, campaign_name=None):

        exact_match_campaigns = None
        print(search_terms["Targeting"])
        # Iterate over search terms
        for index, row in search_terms.iterrows():
            # If not exists in exact match campaigns add it
            if (exact_match_campaigns["Keyword Text"].eq(row["Targeting"])).any():
                continue

    @staticmethod
    def add_phrase_search_terms(search_terms, impact_factor, campaign_name):

        phrase_match_campaigns = None
        print(search_terms["Targeting"])
        # Iterate over search terms
        for index, row in search_terms.iterrows():
            # If not exists in exact match campaigns add it
            if (phrase_match_campaigns["Keyword Text"].eq(row["Targeting"])).any():
                continue

    @staticmethod
    def add_broad_search_terms(search_terms, impact_factor, campaign_name):

        broad_match_campaigns = None
        print(search_terms["Targeting"])
        # Iterate over search terms
        for index, row in search_terms.iterrows():
            # If not exists in exact match campaigns add it
            if (broad_match_campaigns["Keyword Text"].eq(row["Targeting"])).any():
                continue

    @staticmethod
    def add_search_terms(search_terms):
        pass
