
<h1>Search for image using Google Custom Search API and resize & crop the image afterwords using Python</h1>

<p>

Ok, here's the thing, you want to fetch one image from Google Images and you want to resize it and crop it from the middle.<br /><br />

This code enables you to do that.<br /><br />

Except there's four things you need to do before using this peace of code in your project:<br /><br />

1. Setup your Google developers account and project<br />
2. Install dependencies<br />
3. Edit settings.py<br />
4. Define search parameters and image path

</p>

<p>

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
Save your developers key for your project in this variable:<br />
<code>GOOGLE_API_DEVELOPER_KEY</code><br /><br />

Save ID of the custom search engine in this variable:<br />
<code>GOOGLE_API_CUSTOM_SEARCH_CX</code><br /><br />

Define path where you want the image to be saved in this variable:<br />
<code>IMAGE_PATH</code><br /><br />

Define x, y size of your new saved image in this variable:<br />
<code>IMAGE_SIZE</code>

<h2>4. Define search parameters and image</h2>
In run.py define search parameters and image file name. You can find detailed description of search parameters in google_api.py<br />
<code>search_params = {<br />
    'q': '__my_search_query__',<br />
    'num': 5,<br />
    'safe': 'off',<br />
    'fileType': 'jpg',<br />
    'imgType': 'photo',<br />
    'imgSize': 'large',<br />
    'searchType': 'image',<br />
    'imgDominantColor': 'black' <br />
}<br />
path_to_image = settings.IMAGE_PATH[0] % '__my_image__.jpg'</code>

</p>
