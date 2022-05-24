# Changelog

## 1.4.3

### Added in 1.4.3  
-   Travis switched with GitHub Actions

### Fixed in 1.4.2

-   Updated version of google-api-python-client lib

## 1.4.2

### Fixed in 1.4.2

-   Bad referrer link fix
-   Image validation fix (discovered by [@SiewLinYap](https://github.com/SiewLinYap))

### Added in 1.4.2

-   Requests browser simulation

## 1.4.1

### Fixed in 1.4.1

-   Search parameters aligned with Google's definitions (pull request by [@SiewLinYap](https://github.com/SiewLinYap))

### Added in 1.4.1

-   Support for transparent images

## 1.4.0

### Added in 1.4.0

-   Image object now has a referrer url (source) as well

## 1.3.10

### Fixed in 1.3.10

-   Improved error handling when trying to fetch images

## 1.3.9

### Fixed in 1.3.9

-   Added "imgColorType" param for Google API search (pull request by [@SantaHey](https://github.com/SantaHey))

## 1.3.8

### Fixed in 1.3.8

-   Security vulnerability found in Pillow. Update to version to 8.1.1.

## 1.3.7

### Fixed in 1.3.7

-   Handling CLI exception when api key and cx are not provided
-   Handling PIL open and rgb convert exception

## Added in 1.3.7

-   Curses terminal progress is now started and ended using context (with statement)
-   CLI also uses contextual progress
-   Better progress output in CLI overall

## 1.3.6

### Fixed in 1.3.6

-   CLI used non-null default params (discovered by [@itoche](https://github.com/itoche))

## 1.3.5

### Fixed in 1.3.5

-   Pilow version updated (pull request by [@eladavron](https://github.com/eladavron))
-   Fixed x-raw-image://urls (pull request by [@reteps](https://github.com/reteps))

## 1.3.4

### Fixed in 1.3.4

-   Number of images limit would produce error if number was 20 or 30 or etc (issue discovered by [@gaarsmu](https://github.com/gaarsmu))

## 1.3.3

### Fixed in 1.3.3

-   SSL check is back

## 1.3.2

### Fixed in 1.3.2

-   Some images failed to download (issue discovered by [@techguytechtips](https://github.com/techguytechtips))

## 1.3.1

### Added in 1.3.1

-   Option to specify images usage rights (change made by [@bradleyfowler123](https://github.com/bradleyfowler123))

## 1.3.0

### Added in 1.3.0

-   Removed Python 2.7 support

### Fixed in 1.3.0

-   Upgrade from Pillow 6.0 to 7.1.0
-   Fixed issue with downloading images with custom name

## 1.2.1

### Fixed in 1.2.1

-   If Google returns zero results, don't loop to get desired number of images. 

## 1.2.0

### Added in 1.2.0

-   Ability to save save images with custom file name (change suggested by [@otsir](https://github.com/otsir))

## 1.1.4

### Fixed in 1.1.4

-   Sometimes the lib would return more images then user would request.

## 1.1.3

### Fixed in 1.1.3

-   CLI was broken, so I fixed it.

## 1.1.2

### Added in 1.1.2

-   Due to the image validation, non-valid images are ignored, so is triggered again and again until desired number of images is reached (change suggested by [@Uskompuf](https://github.com/Uskompuf)

## 1.1.1

### Added in 1.1.1

-   Automatic paging (change suggested by [@Uskompuf](https://github.com/Uskompuf)
-   Image validation enable/disable

### Fixed in 1.1.1

-   Better exception handling during image check timeout.

## 1.1.0

### Added in 1.1.0

-   Google api search apgination using next searxh parameter (change suggested by [@Uskompuf](https://github.com/Uskompuf)

## 1.0.1  

### Fixed in 1.0.1  

-   Sometimes google api desn't return 'items' in response and code breaks. 

## 1.0.0

### Added in 1.0.0
-   Multithreaded images downloading
-   Download progress bars
-   External progress bar insertion 

## 0.3.8

### Fixed in 0.3.8
-   Non-alphanumeric characters removed from file names which are not valid characters in windows file names (change made by [@sebastianchr](https://github.com/sebastianchr)

## 0.3.7

### Fixed in 0.3.7
-   Code formatted.

## 0.3.6

### Added in 0.3.6
-   Cache_discovery option forward fix.

## 0.3.5

### Added in 0.3.5
-   Cache_discovery option for search method to control file_cache (change made by [@maredov](https://github.com/marodev)).

## 0.3.4

### Fixed added in 0.3.4
-   Dependencies versions updated (change made by [@maredov](https://github.com/marodev))

## 0.3.3

### Fixed in 0.3.3
-   Travis CI definition for PyPi upload.

## 0.3.2

### Fixed in 0.3.2
-   API call default parameter changed from specific to blank (change made by [@mateusrangel](https://github.com/mateusrangel)).

## 0.3.1

### Added in 0.3.1
-   Class docstrings.

## 0.3.0

### Added in 0.3.0
-   Tests added. 

## 0.2.0

### Added in 0.2.0
-   Saving to a BytesIO object (change made by [@fuchsia80](https://github.com/fuchsia80)). 
