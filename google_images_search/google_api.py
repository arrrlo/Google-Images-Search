import os
import copy
import requests
from apiclient.discovery import build


class GoogleCustomSearch(object):
    """Wrapper class for Google images search api"""

    def __init__(self, developer_key=None,
                 custom_search_cx=None,
                 fethch_resize_save=None):

        self._developer_key = developer_key or \
                              os.environ.get('GCS_DEVELOPER_KEY')
        self._custom_search_cx = custom_search_cx or \
                                 os.environ.get('GCS_CX')

        self._google_build = None
        self._search_param_num = 0
        self._fethch_resize_save = fethch_resize_save

        self._search_params_keys = {
            'q': None,
            'searchType': 'image',
            'num': 1,
            'imgType': None,
            'imgSize': None,
            'fileType': None,
            'safe': 'off',
            'imgDominantColor': None
        }

    def _query_google_api(self, search_params, cache_discovery=True):
        """Queries Google api
        :param search_params: dict of params
        :param cache_discovery whether or not to cache the discovery doc
        :return: search result object
        """

        if not self._google_build:
            self._google_build = build("customsearch", "v1",
                                       developerKey=self._developer_key,
                                       cache_discovery=cache_discovery)

        return self._google_build.cse().list(
            cx=self._custom_search_cx, **search_params).execute()

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
                # take user defined param value if defined
                search_params[key] = params_value
            elif value:
                # take default param value if defined
                search_params[key] = value

            if key == 'num':
                # save the original number of num search parameter
                self._search_param_num = copy.copy(int(search_params[key]))

                # add 5 more to number of images to substitute false ones
                search_params[key] = int(search_params[key]) + 5

        return search_params

    def search(self, params, cache_discovery=True):
        """Search for images and returns
        them using generator object
        :param params: search params
        :param cache_discovery whether or not to cache the discovery doc
        :return: yields url to searched image
        """

        search_params = self._search_params(params)

        res = self._query_google_api(search_params, cache_discovery)

        for image in res.get('items'):

            # end if the number of iterations
            # reaches the number parameter of search
            if not self._search_param_num:
                break

            try:
                response = requests.head(image['link'], timeout=5)
                content_length = response.headers.get('Content-Length')

                # check if the url is valid
                if response.status_code == 200 and \
                        'image' in response.headers['Content-Type'] and \
                        content_length:

                    # calculate download chunk size based on image size
                    self._fethch_resize_save.set_chunk_size(
                        image['link'], content_length
                    )

                    # decrease images number counter
                    self._search_param_num -= 1

                    # if everything is ok, yield image url back
                    yield image['link']

                else:
                    # validation failed, go with another image
                    continue

            except requests.exceptions.ConnectTimeout:
                pass
            except requests.exceptions.SSLError:
                pass


class GoogleBackendException(Exception):
    """Exception handler for search api"""
