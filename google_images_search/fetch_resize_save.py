import os
import curses
import requests
import threading
from PIL import Image
from resizeimage import resizeimage

from .google_api import GoogleCustomSearch


class FetchResizeSave(object):
    """Class with resizing and downloading logic"""

    def __init__(self, developer_key, custom_search_cx,
                 progressbar_fn=None, progress=False):

        # initialise google api
        self._google_custom_search = GoogleCustomSearch(
            developer_key, custom_search_cx, self)

        self._search_result = []

        self._stdscr = None
        self._progress = False
        self._chunk_sizes = {}
        self._terminal_lines = {}
        self._download_progress = {}
        self._report_progress = progressbar_fn

        self._set_data()

        if progressbar_fn:
            # user nserted progressbar fn
            self._progress = True
        else:
            if progress:
                # initialise internal progressbar
                self._progress = True
                self._stdscr = curses.initscr()
                self._report_progress = self.__report_progress

    def _set_data(self, search_params=None, path_to_dir=False,
                  width=None, height=None, cache_discovery=True):
        """Set data for Google api search, save and resize
        :param search_params: parameters for Google API Search
        :param path_to_dir: path where the images should be downloaded
        :param width: crop width of the images
        :param height: crop height of the images
        :param cache_discovery: whether or not to cache the discovery doc
        :return: None
        """

        self._width = width
        self._height = height
        self._path_to_dir = path_to_dir
        self._search_params = search_params
        self._cache_discovery = cache_discovery

    def _get_data(self):
        """Get data for Google api search, save and resize
        :return: tuple
        """

        return self._search_params, \
               self._path_to_dir, \
               self._width,\
               self._height,\
               self._cache_discovery

    def search(self, search_params, path_to_dir=False, width=None,
               height=None, cache_discovery=True, clear_prev_results=False):
        """Fetched images using Google API and does the download and resize
        if path_to_dir and width and height variables are provided.
        :param search_params: parameters for Google API Search
        :param path_to_dir: path where the images should be downloaded
        :param width: crop width of the images
        :param height: crop height of the images
        :param cache_discovery: whether or not to cache the discovery doc
        :return: None
        """

        if clear_prev_results:
            self._search_result = list()

        self._set_data(
            search_params, path_to_dir, width, height, cache_discovery
        )

        i = 0
        threads = []
        for url in self._google_custom_search.search(
            search_params, cache_discovery
        ):
            # initialise image object
            image = GSImage(self)
            image.url = url

            # set thread safe variables
            self._download_progress[url] = 0
            self._terminal_lines[url] = i
            i += 2

            # set thread with function and arguments
            thread = threading.Thread(
                target=self._download_and_resize,
                args=(path_to_dir, image, width, height)
            )

            # start thread
            thread.start()

            # register thread
            threads.append(thread)

        # wait for all threads to end here
        for thread in threads:
            thread.join()

        if self._progress:
            if self._stdscr:
                curses.endwin()

    def next_page(self):
        """Get next batch of images.
        Number of images is defined with num search parameter.
        :return: search results
        """

        start = self._search_params.get('start', 1) + \
                self._search_params.get('num', 1)
        self._search_params['start'] = start
        self._search_result = []

        self.search(*self._get_data())


    def set_chunk_size(self, url, content_size):
        """Set images chunk size according to its size
        :param url: image url
        :param content_size: image size
        :return: None
        """

        self._chunk_sizes[url] = int(int(content_size) / 100) + 1

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

        raw_filename = url.split('/')[-1].split('?')[0]
        basename, ext = os.path.splitext(raw_filename)
        filename = "".join(x for x in basename if x.isalnum()) + ext

        path_to_image = os.path.join(path_to_dir, filename)

        with open(path_to_image, 'wb+') as f:
            for chunk in self.get_raw_data(url):
                f.write(chunk)

        return path_to_image

    def get_raw_data(self, url):
        """Generator method for downloading images in chunks
        :param url: url to image
        :return: raw image data
        """

        with requests.get(url, stream=True) as req:
            for chunk in req.iter_content(chunk_size=self._chunk_sizes[url]):

                # filter out keep-alive new chunks
                if chunk:

                    # report progress
                    if self._progress:
                        self._download_progress[url] += 1
                        if self._download_progress[url] <= 100:
                            self._report_progress(url, self._download_progress[url])

                    yield chunk

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

    def __report_progress(self, url, progress):
        """Prints a progress bar in terminal
        :param url:
        :param progress:
        :return:
        """

        self._stdscr.addstr(
            self._terminal_lines[url], 0, "Downloading file: {0}".format(url)
        )
        self._stdscr.addstr(
            self._terminal_lines[url] + 1, 0,
            "Progress: [{1:100}] {0}%".format(progress, "#" * progress)
        )
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

        return b''.join(list(self._fetch_resize_save.get_raw_data(self._url)))

    def copy_to(self, obj, raw_data=None):
        """Copies raw image data to another object, preferably BytesIO
        :param obj: BytesIO
        :param raw_data: raw data
        :return: None
        """

        if not raw_data:
            raw_data = self.get_raw_data()

        obj.write(raw_data)

    def resize(self, width, height):
        """Resize the image
        :param width: int
        :param height: int
        :return: None
        """

        self._fetch_resize_save.__class__.resize(self._path, width, height)
        self.resized = True
