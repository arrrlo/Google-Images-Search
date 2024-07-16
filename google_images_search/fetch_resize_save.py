import os
import curses
import requests
import threading
from PIL import Image, UnidentifiedImageError
from resizeimage import resizeimage, imageexceptions

from .meta import __version__
from .google_api import GoogleCustomSearch


IMAGES_NUM_LIMIT = 10

class FetchResizeSave(object):
    """Class with resizing and downloading logic"""

    def __init__(self, developer_key, custom_search_cx,
                 progressbar_fn=None, validate_images=True, siterestrict=False):

        # initialise google api
        self._google_custom_search = GoogleCustomSearch(
            developer_key, custom_search_cx, self, siterestrict)

        self._search_result = []
        self.validate_images = validate_images

        self._stdscr = None
        self._progress = False
        self._chunk_sizes = {}
        self.zero_return = False
        self._terminal_lines = {}
        self._download_progress = {}
        self._search_for_more = False
        self._report_progress = progressbar_fn

        self._set_data()

        self._page = 1
        self._number_of_images = None

        if progressbar_fn:
            # user inserted progressbar fn
            self._progress = True

    def __enter__(self):
        """Entering a terminal window setup
        :return: self
        """

        self._report_progress = self.__report_progress
        self._progress = True

        # set terminal screen
        self._stdscr = curses.initscr()
        self._stdscr.keypad(True)
        curses.cbreak()
        curses.noecho()

        # show terminal header information
        self._stdscr.addstr(0, 0, f'GOOGLE IMAGES SEARCH {__version__}')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exiting terminal window and putting all back as it was
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """

        self._progress = False

        # reverse all as it was
        self._stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def _set_data(self, search_params=None, path_to_dir=False,
                  width=None, height=None, custom_image_name=None, cache_discovery=True):
        """Set data for Google api search, save and resize
        :param search_params: parameters for Google API Search
        :param path_to_dir: path where the images should be downloaded
        :param width: crop width of the images
        :param height: crop height of the images
        :param custom_image_name: define custom filename
        :param cache_discovery: whether or not to cache the discovery doc
        :return: None
        """

        self._width = width
        self._height = height
        self._path_to_dir = path_to_dir
        self._search_params = search_params
        self._custom_image_name = custom_image_name
        self._cache_discovery = cache_discovery

    def _get_data(self):
        """Get data for Google api search, save and resize
        :return: tuple
        """

        return self._search_params, \
               self._path_to_dir, \
               self._width,\
               self._height,\
               self._custom_image_name, \
               self._cache_discovery

    def search(self, search_params, path_to_dir=False, width=None,
               height=None, custom_image_name=None, cache_discovery=False):
        """Fetched images using Google API and does the download and resize
        if path_to_dir and width and height variables are provided.
        :param search_params: parameters for Google API Search
        :param path_to_dir: path where the images should be downloaded
        :param width: crop width of the images
        :param height: crop height of the images
        :param custom_image_name: define custom filename
        :param cache_discovery: whether or not to cache the discovery doc
        :return: None
        """

        if not self._search_for_more:
            self._set_data(
                search_params, path_to_dir, width, height, custom_image_name,
                cache_discovery
            )
            self._search_result = []

        # number of images required from lib user is important
        # save it only when searching for the first time
        if not self._number_of_images:
            self._number_of_images = search_params.get('num') or 1

        start = self._number_of_images * (self._page - 1)
        end = self._number_of_images * self._page

        for i, page in enumerate(range(start, end, IMAGES_NUM_LIMIT)):
            start = page+1

            if self._number_of_images >= IMAGES_NUM_LIMIT*(i+1):
                num = IMAGES_NUM_LIMIT
            else:
                num = (self._number_of_images % IMAGES_NUM_LIMIT) or \
                      self._number_of_images

            self._search_params['start'] = start
            self._search_params['num'] = num

            self._search_images(*self._get_data())

            if len(self._search_result) >= self._number_of_images \
                    or self.zero_return:
                break
        else:
            # run search again if validation removed some images
            # and desired number of images haven't been reached
            self._next_page()

        self._search_result = self._search_result[:self._number_of_images]

    def _search_images(self, search_params, path_to_dir=False, width=None,
                       height=None, _custom_image_name=None, cache_discovery=False):
        """Fetched images using Google API and does the download and resize
        if path_to_dir and width and height variables are provided.
        :param search_params: parameters for Google API Search
        :param path_to_dir: path where the images should be downloaded
        :param width: crop width of the images
        :param height: crop height of the images
        :param _custom_image_name: define custom filename
        :param cache_discovery: whether or not to cache the discovery doc
        :return: None
        """

        i = 0
        threads = []
        for url, referrer_url in self._google_custom_search.search(
            search_params, cache_discovery
        ):
            # initialise image object
            image = GSImage(self)
            image.url = url
            image.referrer_url = referrer_url

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

    def _next_page(self):
        """Run search again if validation removed some images
        and desired number of images haven't been reached
        :return: None
        """

        # don't reset the data
        self._search_for_more = True

        # get new images
        self.next_page()

        # set reset flag
        self._search_for_more = False

    def next_page(self):
        """Get next batch of images.
        Number of images is defined with num search parameter.
        :return: None
        """

        self._page += 1
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
                try:
                    image.resize(width, height)
                except imageexceptions.ImageSizeError:
                    pass

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

        if not ext:
            ext = '.jpg'

        if self._custom_image_name:
            def increment_naming(dir_list, name, number=0):
                if number:
                    file_name = ''.join([name, '(', str(number), ')', ext])
                else:
                    file_name = ''.join([name, ext])

                if file_name in dir_list:
                    return increment_naming(dir_list, name, number+1)
                else:
                    return file_name

            basename = increment_naming(
                os.listdir(path_to_dir), self._custom_image_name)
        else:
            basename = basename + ext

        path_to_image = os.path.join(path_to_dir, basename)

        with open(path_to_image, 'wb') as f:
            for chunk in self.get_raw_data(url):
                f.write(chunk)

        try:
            Image.open(path_to_image).convert('RGBA')\
                .save(path_to_image, 'png')
        except UnidentifiedImageError:
            pass

        return path_to_image

    def get_raw_data(self, url):
        """Generator method for downloading images in chunks
        :param url: url to image
        :return: raw image data
        """

        # simulate browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/27.0.1453.94 '
                          'Safari/537.36'
        }
        with requests.get(url, stream=True, headers=headers) as req:
            for chunk in req.iter_content(chunk_size=self._chunk_sizes.get(url)):

                # filter out keep-alive new chunks
                if chunk:
                    # report progress
                    if self._progress:
                        self._download_progress[url] += 1
                        if self._download_progress[url] <= 100:
                            self._report_progress(
                                url, self._download_progress[url])

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

        try:
            img = resizeimage.resize_cover(img, [int(width), int(height)])
        except resizeimage.ImageSizeError:
            # error resizing an image
            # image is probably too small
            pass

        img.save(path_to_image, img.format)
        fd_img.close()

    def __report_progress(self, url, progress):
        """Prints a progress bar in terminal
        :param url:
        :param progress:
        :return:
        """

        self._stdscr.addstr(
            self._terminal_lines[url] + 2, 0, "Downloading file: {0}".format(url)
        )
        self._stdscr.addstr(
            self._terminal_lines[url] + 3, 0,
            "Progress: [{1:100}] {0}%".format(progress, "#" * progress)
        )
        self._stdscr.refresh()


class GSImage(object):
    """Class for handling one image"""

    def __init__(self, fetch_resize_save):
        self._fetch_resize_save = fetch_resize_save

        self._url = None
        self._path = None
        self._referrer_url = None

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

    @property
    def referrer_url(self):
        """Returns image referrer url
        :return: referrer_url
        """

        return self._referrer_url

    @referrer_url.setter
    def referrer_url(self, referrer_url):
        """Sets image referrer url
        :param referrer_url: referrer url
        :return: None
        """

        self._referrer_url = referrer_url

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
