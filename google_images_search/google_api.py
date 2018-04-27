
__author__ = 'ivan.arar@gmail.com'

import requests
from apiclient.discovery import build


class GoogleCustomSearch(object):

    def __init__(self, developer_key, custom_search_cx):
        self._developer_key = developer_key
        self._custom_search_cx = custom_search_cx
        self._google_build = None
        self._search_params_keys = [
            'q',                # search query

            'searchType',       # Specifies the search type: image. If unspecified, results are limited to webpages.

            'num',              # Number of search results to return.

            # Restricts results to images of a specified type. Supported values are: clipart (clipart),
            'imgType',
                                # face (face), lineart (lineart), news (news), photo (photo)

            'imgSize',          # Returns images of a specified size. Acceptable values are: "huge": huge, "icon": icon,
                                # "large": large, "medium": medium, "small": small, "xlarge": xlarge, "xxlarge": xxlarge

            'fileType',         # Restricts results to files of a specified extension. A list of file types indexable by
                                # Google can be found in Webmaster Tools

            'safe',             # Search safety level. Acceptable values are: "high": Enables highest level of SafeSearch
                                # filtering, "medium": Enables moderate SafeSearch filtering, "off": Disables SafeSearch
                                # filtering. (default)

            'imgDominantColor',  # Returns images of a specific dominant color. Acceptable values are: "black": black,
                                # "blue": blue, "brown": brown, "gray": gray, "green": green, "pink": pink, "purple": purple,
                                # "teal": teal, "white": white, "yellow": yellow
        ]

    def google_service(self):
        if not self._google_build:
            self._google_build = build("customsearch", "v1", developerKey=self._developer_key)
        return self._google_build

    def search_params(self, params):
        search_params = {}
        for key in self._search_params_keys:
            if key in params:
                search_params[key] = params[key]
        return search_params

    def search(self, params):
        search_params = self.search_params(params)
        res = self.google_service().cse()\
            .list(cx=self._custom_search_cx, **search_params).execute()

        for image in res.get('items'):
            try:
                check = requests.get(image['link'], timeout=5)
                if check.status_code == 200:
                    yield image['link']
            except:
                pass
