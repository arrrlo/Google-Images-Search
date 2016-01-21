
__author__ = 'ivan.arar@gmail.com'


import settings
from fetch_resize_save import FetchResizeSave

if __name__ == '__main__':

    search_params = {
        'q': '__my_search_query__',
        'num': 5,
        'safe': 'off',
        'fileType': 'jpg',
        'imgType': 'photo',
        'imgSize': 'large',
        'searchType': 'image',
        'imgDominantColor': 'black' 
    }
    path_to_image = settings.IMAGE_PATH % '__my_image__.jpg'
    
    success, fail = FetchResizeSave(search_params=search_params, path_to_image=path_to_image).run()

    if success:
        # Do something with this new resized and locally saved image
        print(path_to_image)
    else:
        print(fail)