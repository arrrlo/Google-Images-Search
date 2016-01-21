<h1>Search for image using Google Custom Search API and resize & crop the image afterwords using Python</h1>

Ok, here's the thing, you want to fetch one image from Google Images and you want to resize it and crop it from the middle.<br /><br />

This code enables you to do that.<br /><br />

Except there's four things you need to do before using this peace of code in your project:<br /><br />

1. Setup your Google developers account and project<br />
2. Install dependencies<br />
3. Edit settings.py<br />
4. Define search parameters and image path

<h2>1. Setup your Google developers account and project</h2>
Create your developers acount and create your new project:<br />
https://console.developers.google.com<br />
(Among all of the Google APIs enable "Custom Search API" for your project)<br /><br />

Create custom search engine (ID of the engine is used as "GOOGLE_API_CUSTOM_SEARCH_CX" in settings.py):<br />
https://cse.google.com/cse/all<br />
(In the web form where you create/edit your custom search engine enable "Image search" option and and for "Sites to search" option select "Search the entire web but emphasize included sites")

<h2>2. Install dependencies</h2>
<code>pip install Pillow</code><br />
<code>pip install requests</code><br />
<code>pip install python-resize-image</code><br />
<code>pip install google-api-python-client</code>

<h2>3. Edit settings.py</h2>
<p>Replace "__enter_your_api_key_here__" with your API key:</p>
```python
GOOGLE_API_DEVELOPER_KEY = '__enter_your_api_key_here__'
```

<p>Replace "__enter_your_cx_here__" with your cx:</p>
```python
GOOGLE_API_CUSTOM_SEARCH_CX = '__enter_your_cx_here__'
```

<p>Define path where your new image will be saved:</p>
```python
IMAGE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'images', '%s')
```

<p>Define image size:</p>
```python
IMAGE_SIZE = [260, 260]
```

<h2>4. Define search parameters and image</h2>
In run.py replace "__my_search_query__" with desired search term, replace "__my_image__.jpg" with desired name of the image, and define other search parameters as you like.<br />
You can find detailed description of search parameters in google_api.py<br />
```python
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
path_to_image = settings.IMAGE_PATH[0] % '__my_image__.jpg'
```
