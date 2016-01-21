
__author__ = 'ivan.arar@gmail.com'

import requests
from apiclient.discovery import build

import settings


class GoogleCustomSearch:

    def __init__(self):
        self.google_build = None
        self.search_params = [
            'q',                # search query

            'searchType',       # Specifies the search type: image. If unspecified, results are limited to webpages. 
            
            'num',              # Number of search results to return.
            
            'imgType',          # Restricts results to images of a specified type. Supported values are: clipart (clipart), 
                                # face (face), lineart (lineart), news (news), photo (photo)
            
            'imgSize',          # Returns images of a specified size. Acceptable values are: "huge": huge, "icon": icon, 
                                # "large": large, "medium": medium, "small": small, "xlarge": xlarge, "xxlarge": xxlarge
            
            'fileType',         # Restricts results to files of a specified extension. A list of file types indexable by 
                                # Google can be found in Webmaster Tools
            
            'safe',             # Search safety level. Acceptable values are: "high": Enables highest level of SafeSearch 
                                # filtering, "medium": Enables moderate SafeSearch filtering, "off": Disables SafeSearch 
                                # filtering. (default)
            
            'imgDominantColor', # Returns images of a specific dominant color. Acceptable values are: "black": black, 
                                # "blue": blue, "brown": brown, "gray": gray, "green": green, "pink": pink, "purple": purple, 
                                # "teal": teal, "white": white, "yellow": yellow
        ]

    def google_service(self):
        if not self.google_build:
            self.google_build = build("customsearch", "v1", developerKey=settings.GOOGLE_API_DEVELOPER_KEY)
        return self.google_build

    def set_search_params(self, **kwargs):
        search_params = {}
        for param in self.search_params:
            if param in kwargs:
                search_params[param] = kwargs[param]
        return search_params

    def photo_from_google_image(self, **kwargs):
        search_params = self.set_search_params(**kwargs)

        try:
            res = self.google_service().cse().list(cx=settings.GOOGLE_API_CUSTOM_SEARCH_CX, **search_params).execute()
        except Exception, e:
            return False, e

        for image in res['items']:
            try:
                check = requests.get(image['link'], timeout=5)
                if check.status_code == 200:
                    return image['link'], None
            except:
                pass

        return False, Exception('Haven\'t found image on Google')
