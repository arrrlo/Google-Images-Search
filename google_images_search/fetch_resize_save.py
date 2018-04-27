import os
import shutil
import requests
from PIL import Image
from resizeimage import resizeimage

from .google_api import GoogleCustomSearch


class FetchResizeSave(object):

    def __init__(self, developer_key, custom_search_cx):
        self._google_custom_search = GoogleCustomSearch(developer_key, custom_search_cx)
        self._search_resut = {}

    def search(self, search_params, path_to_dir=False, width=None, height=None):
        image = {}

        for url in self._google_custom_search.search(search_params):
            image['url'] = url
            if path_to_dir:
                path_to_image = self.download(url, path_to_dir)
                image['path'] = path_to_image
                if width and height:
                    self.resize(path_to_image, width, height)

            self._search_resut.append(image)

    def results(self):
        return self._search_resut

    def download(self, url, path_to_dir):
        if not os.path.exists(path_to_dir):
            os.makedirs(path_to_dir)

        req = requests.get(url, stream=True)
        path_to_image = os.path.join(path_to_dir, url.split('/')[-1].split('?')[0])
        with open(path_to_image, 'wb') as f:
            req.raw.decode_content = True
            shutil.copyfileobj(req.raw, f)

        return path_to_image

    def resize(self, path_to_image, width, height):
        fd_img = open(path_to_image, 'r')
        img = Image.open(fd_img)
        img = resizeimage.resize_cover(img, [width, height])
        img.save(path_to_image, img.format)
        fd_img.close()
