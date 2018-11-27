<h1>Google Images Search</h1>

[![PyPI version](https://badge.fury.io/py/Google-Images-Search.svg)](https://badge.fury.io/py/Google-Images-Search)

<p>Ok, here's the thing, you want to fetch one image from Google Images and
    you want to resize it and crop it from the middle<br />This code enables you to do that.</p>

<p>Before you continue you need to setup your Google developers account and project:</p>

<p>https://console.developers.google.com<br />
(Among all of the Google APIs enable "Custom Search API" for your project)<br />

https://cse.google.com/cse/all<br />
(In the web form where you create/edit your custom search engine enable "Image search" option and and for "Sites to search" option select "Search the entire web but emphasize included sites")</p>

<p>After setting up you Google developers account and project you should have
    your developers API key and project CX</p>

<h2>CLI usage</h2>

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

<h2>Programmatic usage</h2>

```python
from google_images_search import GoogleImagesSearch

# if you don't enter api key and cx, the package will try to search
# them from environment variables GCS_DEVELOPER_KEY and GCS_CX
gis = GoogleImagesSearch('your_dev_api_key', 'your_project_cx')

# example: GoogleImagesSearch('ABcDeFGhiJKLmnopqweRty5asdfghGfdSaS4abC', '012345678987654321012:abcde_fghij')

#define search params:
search_params = {
    'q': '...',
    'num': 1-50,
    'safe': 'high|medium|off',
    'fileType': 'jpg|gif|png',
    'imgType': 'clipart|face|lineart|news|photo',
    'imgSize': 'huge|icon|large|medium|small|xlarge|xxlarge',
    'searchType': 'image',
    'imgDominantColor': 'black|blue|brown|gray|green|pink|purple|teal|white|yellow'
}

# this will only search for images:
gis.search(search_params=search_params)

# this will search and download:
gis.search(search_params=search_params, path_to_dir='/path/')

# this will search, download and resize:
gis.search(search_params=search_params, path_to_dir='/path/', width=500, height=500)

# search first, then download and resize afterwards
gis.search(search_params=search_params)
for image in gis.results():
    image.download('/path/')
    image.resize(500, 500)
```

<h2>Saving to a BytesIO object</h2>

```python
from google_images_search import GoogleImagesSearch
from io import BytesIO
from PIL import Image

# in this case we're using PIL to keep the BytesIO as an image object
# this way we don't have to wait for disk save / write times
# the image is simply kept in memory
# this example should display 3 pictures of puppies!

gis = GoogleImagesSearch('your_dev_api_key', 'your_project_cx')

myBytesIO = BytesIO()

gis.search({'q': 'puppies', 'num': 3})
for image in gis.results():
    # here we tell the BytesIO object to go back to address 0
    myBytesIO.seek(0)
    
    # this function writes the image to the object
    image.download_bio(myBytesIO)
    
    # we go back to address 0 again so PIL can read it from start to finish
    myBytesIO.seek(0)
    
    # create a temporary image object
    temp_img = Image.open(myBytesIO)
    
    # show it in the default system photo viewer
    temp_img.show()
```
