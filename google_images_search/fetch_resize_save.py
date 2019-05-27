import os
import shutil
import curses
import requests
import threading
from PIL import Image
from resizeimage import resizeimage

from .google_api import GoogleCustomSearch


class FetchResizeSave(object):
    """Class with resizing and downloading logic"""

    def __init__(self, developer_key, custom_search_cx):
        self._google_custom_search = GoogleCustomSearch(developer_key,
                                                        custom_search_cx)
        self._search_result = list()
        self._global_lock = threading.Lock()
        self._stdscr = curses.initscr()
        self._step = 0

        #curses.noecho()
        #curses.cbreak()

    def search(self, search_params, path_to_dir=False, width=None,
               height=None, cache_discovery=True):
        """Fetched images using Google API and does the download and resize
        if path_to_dir and width and height variables are provided.
        :param search_params: parameters for Google API Search
        :param path_to_dir: path where the images should be downloaded
        :param width: crop width of the images
        :param height: crop height of the images
        :param cache_discovery: whether or not to cache the discovery doc
        :return: None
        """

        threads = list()
        for url in self._google_custom_search.search(
                search_params, cache_discovery
        ):
            image = GSImage(self)
            image.url = url

            thread = threading.Thread(
                target=self._download_and_resize,
                args=(path_to_dir, image, width, height)
            )
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def _download_and_resize(self, path_to_dir, image, width, height):
        """Method used for threading
        :param path_to_dir: path to download dir
        :param image: image object
        :param width: crop width
        :param height: crop height
        :return: None
        """

        if path_to_dir:
            image.download(path_to_dir)
            if width and height:
                image.resize(width, height)
        self._search_result.append(image)

    def results(self):
        """Returns objects of downloaded images
        :return: list
        """

        return self._search_result

    def download(self, url, path_to_dir):
        """Downloads image from url to path dir
        Used only by GSImage class
        :param url: image url
        :param path_to_dir: path to directory where image should be saved
        :return: path to image
        """

        if not os.path.exists(path_to_dir):
            os.makedirs(path_to_dir)

        path_to_image = os.path.join(
            path_to_dir, url.split('/')[-1].split('?')[0]
        )

        with open(path_to_image, 'wb+') as f:
            for chunk in self.get_raw_data(url):
                #self.__class__.copy_to(chunk, f)
                f.write(chunk)

        self._step += 2

        return path_to_image

    def get_raw_data(self, url):
        """Generator method for downloading images in chunks
        :param url: url to image
        :return: raw image data
        """

        progress = 0
        image_length = requests.head(url, timeout=5).headers['Content-Length']
        chunk_size = int(int(image_length)/100)+1

        with requests.get(url, stream=True) as req:
            #req.raise_for_status()
            #req.raw.decode_content = True
            #return req.raw

            for chunk in req.iter_content(chunk_size=chunk_size):
                if chunk:  # filter out keep-alive new chunks
                    progress += 1
                    self._report_progress(self._step, url, progress)
                    yield chunk

    @staticmethod
    def copy_to(raw_data, obj):
        """Copy raw image data to another object, preferably BytesIO
        :param raw_data: raw image data
        :param obj: BytesIO object
        :return: None
        """

        shutil.copyfileobj(raw_data, obj)

    @staticmethod
    def resize(path_to_image, width, height):
        """Resize the image and save it again.
        :param path_to_image: os.path
        :param width: int
        :param height: int
        :return: None
        """

        fd_img = open(path_to_image, 'rb')
        img = Image.open(fd_img)
        img = resizeimage.resize_cover(img, [int(width), int(height)])
        img.save(path_to_image, img.format)
        fd_img.close()

    def _report_progress(self, line, filename, progress):
        self._stdscr.addstr(line, 0, "Downloading file: {0}".format(filename))
        self._stdscr.addstr(line + 1, 0,
                      "Total progress: [{1:100}] {0}%".format(progress,
                                                             "#" * progress))
        self._stdscr.refresh()


class GSImage(object):
    """Class for handling one image"""

    def __init__(self, fetch_resize_save):
        self._fetch_resize_save = fetch_resize_save

        self._url = None
        self._path = None

        self.resized = False

    @property
    def url(self):
        """Returns the image url
        :return: url
        """

        return self._url

    @url.setter
    def url(self, image_url):
        """Sets the image url
        :param image_url: url
        :return: None
        """

        self._url = image_url

    @property
    def path(self):
        """Returns image path
        :return: path
        """

        return self._path

    @path.setter
    def path(self, image_path):
        """Sets image path
        :param image_path: path
        :return: None
        """

        self._path = image_path

    def download(self, path_to_dir):
        """Downloads image from url to path
        :param path_to_dir: path
        :return: None
        """

        self._path = self._fetch_resize_save.download(self._url, path_to_dir)

    def get_raw_data(self):
        """Gets images raw data
        :return: raw data
        """

        return self._fetch_resize_save.get_raw_data(self._url)

    def copy_to(self, obj, raw_data=None):
        """Copies raw image data to another object, preferably BytesIO
        :param obj: BytesIO
        :param raw_data: raw data
        :return: None
        """

        if not raw_data:
            raw_data = self.get_raw_data()

        self._fetch_resize_save.__class__.copy_to(raw_data, obj)

    def resize(self, width, height):
        """Resize the image
        :param width: int
        :param height: int
        :return: None
        """

        self._fetch_resize_save.__class__.resize(self._path, width, height)
        self.resized = True
