import click
from termcolor import cprint
from pyfiglet import figlet_format

from .fetch_resize_save import FetchResizeSave
from .google_api import GoogleBackendException


@click.group()
@click.pass_context
@click.option('-k', '--developer_key', help='Developer API key')
@click.option('-c', '--custom_search_cx', help='Custom Search CX')
def cli(ctx, developer_key, custom_search_cx):
    ctx.obj = {
        'object': FetchResizeSave(developer_key, custom_search_cx)
    }


IMAGE_TYPES = ('clipart', 'face', 'lineart', 'news', 'photo', )
IMAGE_SIZES = ('huge', 'icon', 'large', 'medium', 'small', 'xlarge', 'xxlarge', )
FILE_TYPES = ('jpg', 'gif', 'png')
DOMINANT_COLORS = ('black', 'blue', 'brown', 'gray', 'green', 'pink', 'purple',
                   'teal', 'white', 'yellow')
SAFE_SEARCH = ('high', 'medium', 'off', )


@cli.command()
@click.pass_context
@click.option('-q', '--query', help='Search query')
@click.option('-n', '--num', default=5, help='Number of images in response')
@click.option('-s', '--safe', type=click.Choice(SAFE_SEARCH), default='off',
              help='Search safety level')
@click.option('-f', '--filetype', type=click.Choice(FILE_TYPES), default='jpg',
              help='Images file type')
@click.option('-i', '--imagetype', type=click.Choice(IMAGE_TYPES), default='photo',
              help='Image type')
@click.option('-s', '--imagesize', type=click.Choice(IMAGE_SIZES), default='large',
              help='Image size')
@click.option('-c', '--dominantcolor', type=click.Choice(DOMINANT_COLORS),
              default='black', help='Dominant color in images')
@click.option('-d', '--download_path', type=click.Path(dir_okay=True), help='Download images')
@click.option('-w', '--width', help='Image crop width')
@click.option('-h', '--height', help='Image crop height')
def search(ctx, query, num, safe, filetype, imagetype,
           imagesize, dominantcolor, download_path, width, height):

    search_params = {
        'q': query,
        'num': num,
        'safe': safe,
        'fileType': filetype,
        'imgType': imagetype,
        'imgSize': imagesize,
        'imgDominantColor': dominantcolor
    }

    click.clear()

    cprint(figlet_format('Google Images Search', width=120), 'red')
    click.secho(' '*80 + 'by Ivan Arar', fg='red')

    click.echo('-'*120)

    try:
        ctx.obj['object'].search(search_params, download_path, width, height)

        for i, image in enumerate(ctx.obj['object'].results()):
            click.echo(image.url)
            if image.path:
                click.secho(image.path, fg='blue')
                if not image.resized:
                    click.secho('[image is not resized]', fg='red')
            else:
                click.secho('[image is not download]', fg='red')
            click.echo()

    except GoogleBackendException:
        click.secho('Error occured trying to fetch images from Google. Please try again.', fg='red')
        return

    click.echo('-'*120)
    click.echo()
