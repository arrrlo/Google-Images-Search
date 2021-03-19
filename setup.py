import os
from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


def version():
    with open(os.path.join('.', 'google_images_search', 'meta.py')) as f:
        contents = f.read()
    return contents.split('__version__ = ')[1].strip()[1:-1]


setup(
    name='Google Images Search',
    version=version(),

    description='Search for image using Google Custom Search '
                'API and resize & crop the image afterwords',
    long_description=readme(),
    long_description_content_type='text/markdown',

    url='https://github.com/arrrlo/Google-Images-Search',
    licence='MIT',

    author='Ivan Arar',
    author_email='ivan.arar@gmail.com',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='google images, resize, crop',

    packages=['google_images_search'],
    install_requires=[
        'colorama~=0.4',
        'pyfiglet~=0.8',
        'termcolor~=1.1',
        'click~=7.0',
        'six~=1.12',
        'requests~=2.21',
        'Pillow>=8.1.1',
        'python-resize-image~=1.1',
        'google-api-python-client~=1.7',
    ],

    entry_points={
        'console_scripts': [
            'gimages=google_images_search.cli:cli'
        ],
    },

    project_urls={
        'Source': 'https://github.com/arrrlo/Google-Images-Search',
    },
)
