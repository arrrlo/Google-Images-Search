import os
import requests
from apiclient.discovery import build


class GoogleCustomSearch(object):

    def __init__(self, developer_key=None,
                 custom_search_cx=None):

        self._developer_key = developer_key or \
                              os.environ.get('GCS_DEVELOPER_KEY')
        self._custom_search_cx = custom_search_cx or \
                                 os.environ.get('GCS_CX')

        self._google_build = None

        self._search_params_keys = {
            'q': None,
            'searchType': 'image',
            'num': 5,
            'imgType': 'photo',
            'imgSize': 'large',
            'fileType': 'jpg',
            'safe': 'off',
            'imgDominantColor': None
        }

    def _query_google_api(self, search_params):
        if not self._google_build:
            self._google_build = build("customsearch", "v1",
                                       developerKey=self._developer_key)

        return self._google_build.cse().list(
            cx=self._custom_search_cx, **search_params).execute()

    def _search_params(self, params):
        search_params = {}

        for key, value in self._search_params_keys.items():
            params_value = params.get(key)
            if params_value:
                search_params[key] = params_value
            elif value:
                search_params[key] = value

        return search_params

    def search(self, params):
        search_params = self._search_params(params)

        try:
            res = self._query_google_api(search_params)
        except:
            raise GoogleBackendException()

        for image in res.get('items'):
            try:
                check = requests.get(image['link'], timeout=5)
                if check.status_code == 200:
                    yield image['link']
            except:
                pass


class GoogleBackendException(Exception):
    pass