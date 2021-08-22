![Google Images Search](google.jpeg)

# Google Images Search

[![PyPI version](https://badge.fury.io/py/Google-Images-Search.svg)](https://badge.fury.io/py/Google-Images-Search)
[![Build Status](https://travis-ci.com/arrrlo/Google-Images-Search.svg?branch=master)](https://travis-ci.com/arrrlo/Google-Images-Search)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b3d5259c67ca48a7bfe844b9721b6c19)](https://www.codacy.com/app/arrrlo/Google-Images-Search?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=arrrlo/Google-Images-Search&amp;utm_campaign=Badge_Grade)

![GitHub issues](https://img.shields.io/github/issues/arrrlo/Google-Images-Search.svg)
![GitHub closed issues](https://img.shields.io/github/issues-closed/arrrlo/Google-Images-Search.svg)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/arrrlo/Google-Images-Search.svg)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Google-Images-Search.svg)
![GitHub](https://img.shields.io/github/license/arrrlo/Google-Images-Search.svg?color=blue)
![GitHub last commit](https://img.shields.io/github/last-commit/arrrlo/Google-Images-Search.svg?color=blue)

## [Installation](#installation)

To be able to use this library, you need to enable Google Custom Search API, generate API key credentials and set a project:

-   Visit [https://console.developers.google.com](https://console.developers.google.com) and create a project.

-   Visit [https://console.developers.google.com/apis/library/customsearch.googleapis.com](https://console.developers.google.com/apis/library/customsearch.googleapis.com) and enable "Custom Search API" for your project.

-   Visit [https://console.developers.google.com/apis/credentials](https://console.developers.google.com/apis/credentials) and generate API key credentials for your project.

-   Visit [https://cse.google.com/cse/all](https://cse.google.com/cse/all) and in the web form where you create/edit your custom search engine enable "Image search" option and for "Sites to search" option select "Search the entire web but emphasize included sites".  

After setting up your Google developers account and project you should have been provided with developers API key and project CX.

Install package from pypi.org:  

```bash
> pip install Google-Images-Search
```

## [CLI usage](#cli-usage)

```bash
# without environment variables:

> gimages -k __your_dev_api_key__ -c __your_project_cx__ search -q puppies
```

```bash
# with environment variables:

> export GCS_DEVELOPER_KEY=__your_dev_api_key__
> export GCS_CX=__your_project_cx__
>
> gimages search -q puppies
```

```bash
# search only (no download and resize):

> gimages search -q puppies
```

```bash
# search and download only (no resize):

> gimages search -q puppies -d /path/on/your/drive/where/images/should/be/downloaded
```

```bash
# search, download and resize:

> gimages search -q puppies -d /path/ -w 500 -h 500
```

## [Programmatic usage](#programmatic-usage)

```python
from google_images_search import GoogleImagesSearch

# you can provide API key and CX using arguments,
# or you can set environment variables: GCS_DEVELOPER_KEY, GCS_CX
gis = GoogleImagesSearch('your_dev_api_key', 'your_project_cx')

# define search params:
_search_params = {
    'q': '...',
    'num': 10,
    'safe': 'high|medium|off',
    'fileType': 'jpg|gif|png',
    'imgType': 'clipart|face|lineart|news|photo',
    'imgSize': 'huge|icon|large|medium|small|xlarge|xxlarge',
    'imgDominantColor': 'black|blue|brown|gray|green|orange|pink|purple|red|teal|white|yellow',
    'imgColorType': 'color|gray|mono|trans',
    'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived'
}

# this will only search for images:
gis.search(search_params=_search_params)

# this will search and download:
gis.search(search_params=_search_params, path_to_dir='/path/')

# this will search, download and resize:
gis.search(search_params=_search_params, path_to_dir='/path/', width=500, height=500)

# search first, then download and resize afterwards:
gis.search(search_params=_search_params)
for image in gis.results():
    image.download('/path/')
    image.resize(500, 500)
```

## [Custom file name](#custom-file-name)

Sometimes you would want to save images with file name of your choice.

```python
from google_images_search import GoogleImagesSearch

gis = GoogleImagesSearch('your_dev_api_key', 'your_project_cx')

_search_params = { ... }

gis.search(search_params=_search_params, path_to_dir='...', 
           custom_image_name='my_image')
```

## [Paging](#paging)

Google's API limit is 10 images per request.  
That means if you want 123 images, it will be divided internally into 13 requests.  
Keep in mind that getting 123 images will take a bit more time if the image validation is enabled.

```python
from google_images_search import GoogleImagesSearch

gis = GoogleImagesSearch('your_dev_api_key', 'your_project_cx')
_search_params = {
    'q': '...',
    'num': 123,
}

# get first 123 images:
gis.search(search_params=_search_params)

# take next 123 images from Google images search:
gis.next_page()
for image in gis.results():
    ...
```

## [Image validation](#image-validation)

Every image URL is validated by default.  
That means that every image URL will be checked if the headers can be fetched and validated.  
With that you don't need to wary about which image URL is actually downloadable or not.  
The downside is the time needed to validate.  
If you prefer, you can turn it off.

```python
from google_images_search import GoogleImagesSearch

# turn the validation off with "validate_images" agrument
gis = GoogleImagesSearch('your_dev_api_key', 'your_project_cx', validate_images=False)
```

## [Inserting custom progressbar function](#progressbar)

By default, progressbar is not enabled.  
Only in CLI progressbar is enabled by default using [Curses library](https://docs.python.org/3/howto/curses.html).  
In a programmatic mode it can be enabled in two ways:  
- using contextual mode (Curses)  
- using your custom progressbar function  

```python
from google_images_search import GoogleImagesSearch

# using your custom progressbar function
def my_progressbar(url, progress):
    print(url + ' ' + progress + '%')
gis = GoogleImagesSearch(
    'your_dev_api_key', 'your_project_cx', progressbar_fn=my_progressbar
)
_search_params = {...}
gis.search(search_params=_search_params)

# using contextual mode (Curses)
with GoogleImagesSearch('your_dev_api_key', 'your_project_cx') as gis:
    _search_params = {...}
    gis.search(search_params=_search_params)
...
```

## [Saving to a BytesIO object](#bytes-io)

```python
from google_images_search import GoogleImagesSearch
from io import BytesIO
from PIL import Image

# in this case we're using PIL to keep the BytesIO as an image object
# that way we don't have to wait for disk save / write times
# the image is simply kept in memory
# this example should display 3 pictures of puppies!

gis = GoogleImagesSearch('your_dev_api_key', 'your_project_cx')

my_bytes_io = BytesIO()

gis.search({'q': 'puppies', 'num': 3})
for image in gis.results():
    # here we tell the BytesIO object to go back to address 0
    my_bytes_io.seek(0)

    # take raw image data
    raw_image_data = image.get_raw_data()

    # this function writes the raw image data to the object
    image.copy_to(my_bytes_io, raw_image_data)

    # or without the raw data which will be automatically taken
    # inside the copy_to() method
    image.copy_to(my_bytes_io)

    # we go back to address 0 again so PIL can read it from start to finish
    my_bytes_io.seek(0)

    # create a temporary image object
    temp_img = Image.open(my_bytes_io)
    
    # show it in the default system photo viewer
    temp_img.show()
```
