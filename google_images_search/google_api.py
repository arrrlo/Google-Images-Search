import os
import requests
from apiclient import discovery


class GoogleCustomSearch(object):
    """Wrapper class for Google images search api"""

    def __init__(self, developer_key=None,
                 custom_search_cx=None,
                 fetch_resize_save=None, siterestrict=False):

        self._developer_key = developer_key or \
                              os.environ.get('GCS_DEVELOPER_KEY')
        self._custom_search_cx = custom_search_cx or \
                                 os.environ.get('GCS_CX')

        self._google_build = None
        self._fetch_resize_save = fetch_resize_save
        self.siterestrict = siterestrict

        self._search_params_keys = {
            'q': None,
            'searchType': 'image',
            'num': 1,
            'start': 1,
            'imgType': None,
            'imgSize': None,
            'fileType': None,
            'safe': 'off',
            'imgDominantColor': None,
            'imgColorType': None,
            'rights': None
        }

    def _query_google_api(self, search_params, cache_discovery=True):
        """Queries Google api
        :param search_params: dict of params
        :param cache_discovery whether or not to cache the discovery doc
        :return: search result object
        """

        if not self._google_build:
            self._google_build = discovery.build(
                "customsearch", "v1",
                # discoveryServiceUrl="https://www.googleapis.com/discovery/v1/apis/" "{api}/{apiVersion}/rest",
                developerKey=self._developer_key,
                cache_discovery=cache_discovery)
        req = self._google_build.cse().list(
            cx=self._custom_search_cx, **search_params)
        if self.siterestrict:
            req.uri = req.uri.replace('/v1?', '/v1/siterestrict?')
        return req.execute()


        # return self._google_build.cse().list(
        #     cx=self._custom_search_cx, **search_params).execute()

    def _search_params(self, params):
        """Received a dict of params and merges
        it with default params dict
        :param params: dict
        :return: dict
        """

        search_params = {}

        for key, value in self._search_params_keys.items():
            params_value = params.get(key)

            if params_value:
                if key == "imgSize" and params_value != "imgSizeUndefined":
                    params_value = params_value.upper()
                # take user defined param value if defined
                search_params[key] = params_value
            elif value:
                # take default param value if defined
                search_params[key] = value

        return search_params

    def search(self, params, cache_discovery=False):
        """Search for images and returns
        them using generator object
        :param params: search params
        :param cache_discovery whether or not to cache the discovery doc
        :return: image list
        """

        search_params = self._search_params(params)
        res = self._query_google_api(search_params, cache_discovery)

        results = res.get('items', [])
        if not results:
            self._fetch_resize_save.zero_return = True

        for image in results:
            if len(self._fetch_resize_save._search_result) >= \
                   self._fetch_resize_save._number_of_images:
                break

            if self._fetch_resize_save.validate_images:
                try:
                    # simulate browser request
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/27.0.1453.94 '
                                      'Safari/537.36'
                    }
                    response = requests.head(
                        image['link'], timeout=5, allow_redirects=False,
                        headers=headers
                    )
                    content_length = response.headers.get('Content-Length')
                    content_type = response.headers.get('Content-Type', '')

                    # check if the url is valid
                    if response.status_code == 200 and \
                            'image' in content_type and content_length:

                        # calculate download chunk size based on image size
                        self._fetch_resize_save.set_chunk_size(
                            image['link'], content_length
                        )
                    else:
                        continue
                except requests.exceptions.RequestException:
                    continue

            yield image['link'], image['image']['contextLink']


class GoogleBackendException(Exception):
    """Exception handler for search api"""
