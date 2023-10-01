import settings
from amz_ppc_optimizer import AmzSheetHandler


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
        if AmzSheetHandler.is_keyword_exists(datagram, keyword, "Exact") is False:
            bid = float(row["Cost Per Click (CPC)"])
            datagram = AmzSheetHandler.add_keyword(datagram, exact_camp_name, exact_camp_name, keyword,
                                                   bid * bid_factor, "Exact")
            datagram = AmzSheetHandler.add_keyword(datagram, phrase_camp_name, phrase_camp_name, keyword,
                                                   bid * bid_factor, "Phrase")
            datagram = AmzSheetHandler.add_keyword(datagram, broad_camp_name, broad_camp_name, keyword,
                                                   bid * bid_factor, "Broad")

    return datagram
