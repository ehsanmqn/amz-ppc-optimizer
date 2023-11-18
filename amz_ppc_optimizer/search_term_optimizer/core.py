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
    def add_search_terms(datagram, search_terms, bid_factor):
        # Add profitable search terms to exact campaigns
        exact_camp_name = settings.DEFAULT_EXACT_ST_CAMPAIGN_NAME
        if AmzSheetHandler.is_campaign_exists(datagram, exact_camp_name) is False:
            datagram = AmzSheetHandler.add_campaign(datagram, exact_camp_name, exact_camp_name)

        # Add profitable search terms to phrase campaigns
        phrase_camp_name = settings.DEFAULT_PHRASE_ST_CAMPAIGN_NAME
        if AmzSheetHandler.is_campaign_exists(datagram, phrase_camp_name) is False:
            datagram = AmzSheetHandler.add_campaign(datagram, phrase_camp_name, phrase_camp_name)

        # Add profitable search terms to broad campaigns
        broad_camp_name = settings.DEFAULT_BROAD_ST_CAMPAIGN_NAME
        if AmzSheetHandler.is_campaign_exists(datagram, broad_camp_name) is False:
            datagram = AmzSheetHandler.add_campaign(datagram, broad_camp_name, broad_camp_name)

        for index, row in search_terms.iterrows():
            keyword = row["Customer Search Term"]
            product_ad = AmzSheetHandler.get_product_ad_by_campaign(datagram, row["Campaign Name"], row["Ad Group Name"])
            product_sku = product_ad["SKU"].str

            if AmzSheetHandler.is_keyword_exists(datagram, keyword, "Exact") is False:
                if AmzSheetHandler.is_product_ad_exists(datagram, exact_camp_name, exact_camp_name, product_sku) is False:
                    AmzSheetHandler.add_product_ad(datagram, exact_camp_name, exact_camp_name, product_sku)
                    AmzSheetHandler.add_product_ad(datagram, phrase_camp_name, phrase_camp_name, product_sku)
                    AmzSheetHandler.add_product_ad(datagram, broad_camp_name, broad_camp_name, product_sku)

                bid = float(row["Cost Per Click (CPC)"])
                datagram = AmzSheetHandler.add_keyword(datagram, exact_camp_name, exact_camp_name, keyword,
                                                       bid * bid_factor, "Exact")
                datagram = AmzSheetHandler.add_keyword(datagram, phrase_camp_name, phrase_camp_name, keyword,
                                                       bid * bid_factor, "Phrase")
                datagram = AmzSheetHandler.add_keyword(datagram, broad_camp_name, broad_camp_name, keyword,
                                                       bid * bid_factor, "Broad")

        return datagram
