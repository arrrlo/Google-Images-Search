import click
import googleapiclient

from .google_api import GoogleBackendException
from .fetch_resize_save import FetchResizeSave, __version__


@click.group()
@click.pass_context
@click.option('-k', '--developer_key', help='Developer API key')
@click.option('-c', '--custom_search_cx', help='Custom Search CX')
def cli(ctx, developer_key, custom_search_cx):
    click.echo()
    click.secho(f'GOOGLE IMAGES SEARCH {__version__}', fg='yellow')
    click.echo()

    ctx.obj = {
        'object': FetchResizeSave(
            developer_key, custom_search_cx
        )
    }


IMAGE_TYPES = ('clipart', 'face', 'lineart', 'stock', 'photo',
               'animated', 'imgTypeUndefined')
IMAGE_SIZES = ('huge', 'icon', 'large', 'medium', 'small',
               'xlarge', 'xxlarge', 'imgSizeUndefined')
FILE_TYPES = ('jpg', 'gif', 'png')
DOMINANT_COLORS = ('black', 'blue', 'brown', 'gray', 'green', 'pink', 'purple',
                   'teal', 'white', 'yellow')
SAFE_SEARCH = ('active', 'high', 'medium', 'off', 'safeUndefined')
USAGE_RIGHTS = ('cc_publicdomain', 'cc_attribute', 'cc_sharealike',
                'cc_noncommercial', 'cc_nonderived')


@cli.command()
@click.pass_context
@click.option('-q', '--query', help='Search query')
@click.option('-n', '--num', default=1, help='Number of images in response')
@click.option('-s', '--safe', type=click.Choice(SAFE_SEARCH),
              default='off', help='Search safety level')
@click.option('-f', '--filetype', type=click.Choice(FILE_TYPES),
              help='Images file type')
@click.option('-i', '--imagetype', type=click.Choice(IMAGE_TYPES),
              help='Image type')
@click.option('-s', '--imagesize', type=click.Choice(IMAGE_SIZES),
              help='Image size')
@click.option('-c', '--dominantcolor', type=click.Choice(DOMINANT_COLORS),
              help='Dominant color in images')
@click.option('-r', '--usagerights', type=click.Choice(USAGE_RIGHTS),
              multiple=True, help='Usage rights of images')
@click.option('-d', '--download_path', type=click.Path(dir_okay=True),
              help='Download images')
@click.option('-w', '--width', help='Image crop width')
@click.option('-h', '--height', help='Image crop height')
@click.option('-m', '--custom_file_name', help='Custom file name')
def search(ctx, query, num, safe, filetype, imagetype, imagesize,
           dominantcolor, usagerights, download_path, width, height,
           custom_file_name):

    usagerights = '|'.join(usagerights)
    if imagesize:
        imagesize = imagesize.upper()
    search_params = {
        'q': query,
        'num': num,
        'safe': safe,
        'fileType': filetype,
        'imgType': imagetype,
        'rights': usagerights,
        'imgSize': imagesize,
        'imgDominantColor': dominantcolor
    }

    try:
        gis = ctx.obj['object']

        with gis:
            gis.search(search_params, download_path,
                       width, height, custom_file_name)

        results = ctx.obj['object'].results()

        if results:
            for image in results:
                click.echo(image.url)
                if image.path:
                    click.secho(image.path, fg='blue')
                    if not image.resized:
                        click.secho('[image is not resized]', fg='red')
                else:
                    click.secho('[image is not downloaded]', fg='red')
                click.echo()
        else:
            click.secho('No images found!', fg='red')

    except GoogleBackendException:
        click.secho('Error occurred trying to fetch '
                    'images from Google. Please try again.', fg='red')

    except googleapiclient.errors.HttpError as e:
        click.secho(f'Google reported an error: {str(e)}', fg='red')
        return
