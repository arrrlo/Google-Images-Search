import os
import shutil
import requests
from PIL import Image
from resizeimage import resizeimage

from .google_api import GoogleCustomSearch


class FetchResizeSave(object):

    def __init__(self, developer_key, custom_search_cx):
        self._google_custom_search = GoogleCustomSearch(developer_key, custom_search_cx)
        self._search_resut = []

    def search(self, search_params, path_to_dir=False, width=None, height=None):
        for url in self._google_custom_search.search(search_params):

            image = GSImage(self)
            image.url = url

            if path_to_dir:
                image.download(path_to_dir)
                if width and height:
                    image.resize(width, height)

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
        try:
            fd_img = open(path_to_image, 'rb')
            img = Image.open(fd_img)
            img = resizeimage.resize_cover(img, [int(width), int(height)])
            img.save(path_to_image, img.format)
            fd_img.close()
        except resizeimage.ImageSizeError as e:
            pass


class GSImage(object):

    def __init__(self, fetch_resize_save):
        self._fetch_resize_save = fetch_resize_save

        self._url = None
        self._path = None

        self.resized = False

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, image_url):
        self._url = image_url

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, image_path):
        self._path = image_path

    def download(self, path_to_dir):
        self._path = self._fetch_resize_save.download(self._url, path_to_dir)

    def resize(self, width, height):
        self._fetch_resize_save.resize(self._path, width, height)
        self.resized = True
