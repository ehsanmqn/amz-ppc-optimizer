class SearchTermOptimizer:
    """
    Placement Optimizer
    """

    _data_sheet = None

    def __init__(self, data):
        self._data_sheet = data

    @property
    def datasheet(self):
        return self._data_sheet

    def find_profitable_search_terms(self, desired_acos):
        """
        Return search terms that have ACOS lower than desired ACOS
        :return:
        """

        search_terms = self._data_sheet[self._data_sheet["Match Type"].isin(["EXACT", "PHRASE", "BROAD"])]
        result = search_terms[(search_terms["Total Advertising Cost of Sales (ACOS) "] < desired_acos) & (
                search_terms["Total Advertising Cost of Sales (ACOS) "] > 0)]
        result = result.sort_values(by=["Total Advertising Cost of Sales (ACOS) "], ascending=False)

        return result

    def find_unprofitable_search_terms(self, desired_acos):
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
    def add_search_terms(search_terms, impact_factor,
                         exact_match_campaigns, exact_match_nominated,
                         phrase_match_campaigns, phrase_match_add_nominated,
                         broad_match_campaigns, broad_match_nominated):

        # Iterate over search terms
        for index, row in search_terms.iterrows():
            # If not exists in exact match campaigns add it
            if (exact_match_campaigns["Keyword Text"].eq(row["Targeting"])).any():
                continue

            # If not exists in phrase match campaigns add it
            if (phrase_match_campaigns["Keyword Text"].eq(row["Targeting"])).any():
                continue

            # If not exists in broad match campaigns add it
            if (broad_match_campaigns["Keyword Text"].eq(row["Targeting"])).any():
                continue
