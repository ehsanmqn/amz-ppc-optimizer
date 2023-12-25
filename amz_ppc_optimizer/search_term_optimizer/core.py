from amz_ppc_optimizer import AmzSheetHandler, settings


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
        # Iterate over search terms
        for index, row in search_terms.iterrows():
            # If not exists in exact match campaigns add it
            if (exact_match_campaigns["Keyword Text"].eq(row["Targeting"])).any():
                continue

    @staticmethod
    def add_phrase_search_terms(search_terms, impact_factor, campaign_name):

        phrase_match_campaigns = None
        # Iterate over search terms
        for index, row in search_terms.iterrows():
            # If not exists in exact match campaigns add it
            if (phrase_match_campaigns["Keyword Text"].eq(row["Targeting"])).any():
                continue

    @staticmethod
    def add_broad_search_terms(search_terms, impact_factor, campaign_name):

        broad_match_campaigns = None
        # Iterate over search terms
        for index, row in search_terms.iterrows():
            # If not exists in exact match campaigns add it
            if (broad_match_campaigns["Keyword Text"].eq(row["Targeting"])).any():
                continue

    @staticmethod
    def add_search_terms(datagram, search_terms, bid_factor, products_portfolio):
        for index, row in search_terms.iterrows():
            customer_st = AmzSheetHandler.get_customer_search_term(row)
            st_product = AmzSheetHandler.get_search_term_targeting_portfolio(row)
            st_bid = float(AmzSheetHandler.get_search_term_cpc(row))

            add_campaign = products_portfolio[st_product]["search_terms_campaign"]
            add_ad_group = products_portfolio[st_product]["search_terms_ad_group"]
            add_campaign_id = products_portfolio[st_product]["search_terms_campaign_id"]
            add_ad_group_id = products_portfolio[st_product]["search_terms_ad_group_id"]

            if AmzSheetHandler.is_keyword_exists(datagram, customer_st, "Exact") is False:
                datagram = AmzSheetHandler.add_keyword(datagram, add_campaign_id, add_ad_group_id, customer_st, st_bid * bid_factor, "Exact")

            if AmzSheetHandler.is_keyword_exists(datagram, customer_st, "Phrase") is False:
                datagram = AmzSheetHandler.add_keyword(datagram, add_campaign_id, add_ad_group_id, customer_st, st_bid * bid_factor, "Phrase")

            if AmzSheetHandler.is_keyword_exists(datagram, customer_st, "Broad") is False:
                datagram = AmzSheetHandler.add_keyword(datagram, add_campaign_id, add_ad_group_id, customer_st, st_bid * bid_factor, "Broad")

        return datagram
