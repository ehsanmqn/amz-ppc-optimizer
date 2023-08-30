import logging
from ad_api.base import AdvertisingApiException
from ad_api.api import sponsored_products
from ad_api.base import Marketplaces


class AmzPpcWrapper:
    _credentials = None
    _campaigns = None

    def __init__(self, refresh_token, client_id, client_secret, profile_id):
        self.credentials = dict(
            refresh_token=refresh_token,
            client_id=client_id,
            client_secret=client_secret,
            profile_id=profile_id,
        )

    @property
    def credentials(self):
        return self._credentials

    @credentials.setter
    def credentials(self, credential_data: dict):
        self._credentials = credential_data

    @property
    def campaigns(self):
        payload = None

        try:
            status = 'enabled'
            result = sponsored_products.Campaigns(credentials=self.credentials,
                                                  debug=True,
                                                  marketplace=Marketplaces.AE).list_campaigns(
                stateFilter=status
            )

            payload = result.payload
            logging.info(payload)

        except AdvertisingApiException as error:
            logging.info(error)

        return payload
