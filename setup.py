from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='Google Images Search',
    version="0.3.3",

    description='Search for image using Google Custom Search API and resize & crop the image afterwords',
    long_description=readme(),
    long_description_content_type='text/markdown',

    url='https://github.com/arrrlo/Google-Images-Search',
    licence='MIT',

    author='Ivan Arar',
    author_email='ivan.arar@gmail.com',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='google images, resize, crop',

    packages=['google_images_search'],
    install_requires=[
        'colorama~=0.3',
        'pyfiglet~=0.7.5',
        'termcolor~=1.1.0',
        'click==6.3',
        'six~=1.11.0',
        'requests~=2.20.0',
        'Pillow~=5.2.0',
        'python-resize-image~=1.1.11',
        'google-api-python-client~=1.6.6',
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
