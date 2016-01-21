
<h1>Search for image using Google Custom Search API and resize & crop the image afterwords</h1>

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
https://console.developers.google.com<br /><br />

Create custom search engine (ID of engine is used as "cx" parameter in code):<br />
https://cse.google.com/cse/all<br />
(In the web form where you create/edit your custom search engine enable "Image search" option and and for "Sites to search" option select "Search the entire web but emphasize included sites")

<h2>2. Install dependencies</h2>
<code>pip install Pillow</code><br />
<code>pip install requests</code><br />
<code>pip install python-resize-image</code><br />
<code>pip install google-api-python-client</code>

<h2>3. Edit settings.py</h2>


<h2>4. Define search parameters and image</h2>


</p>
