
__author__ = 'ivan.arar@gmail.com'


import os
import shutil
import requests
from PIL import Image
from resizeimage import resizeimage

import settings
from google_api import GoogleCustomSearch


class FetchResizeSave:

    def __init__(self, search_params, path_to_image):
        self.search_params = search_params
        self.path_to_image = path_to_image
        self.google_custom_search = GoogleCustomSearch()

    def run(self):
        image_from_google, google_exception = self.google_custom_search.photo_from_google_images(**self.search_params)

        if not image_from_google:
            return False, google_exception
        else:
            dir_to_image = '/'.join(self.path_to_image.split('/')[:-1])
            if not os.path.exists(dir_to_image):
                os.makedirs(dir_to_image)

            req = requests.get(image_from_google, stream=True)
            if req.status_code == 200:
                with open(self.path_to_image, 'wb') as file_on_disk:
                    req.raw.decode_content = True
                    shutil.copyfileobj(req.raw, file_on_disk)

            fd_img = open(self.path_to_image, 'r')
            img = Image.open(fd_img)
            img = resizeimage.resize_cover(img, settings.IMAGE_SIZE)
            img.save(self.path_to_image, img.format)
            fd_img.close()

            return True, None