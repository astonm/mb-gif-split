import click
import os
import requests

from cStringIO import StringIO
from PIL import Image, ImageSequence

@click.command()
@click.argument('path_or_url')
@click.option('--o', help="output filename", default=None)
def gif_to_sprites(path_or_url, o):
    filename = os.path.basename(path_or_url).replace(".gif",'')
    f = open_file_or_url(path_or_url)
    im = Image.open(f)

    frames = ImageSequence.Iterator(im)
    frame_width, frame_height = 0, 0
    frame_width, frame_height = frames[0].size

    width = frame_width*len(list(frames))
    height = frame_height
    out = Image.new('RGBA', (width, height))

    f.seek(0)
    im = Image.open(f)
    for i, frame in enumerate(ImageSequence.Iterator(im)):
        out.paste(frame, (frame_width*i, 0))

    out_filename = filename + '_sprite.gif' if o is None else o
    out.save(out_filename)

    print "use like this:"
    print """
game.load('mySpriteNickname', '%(filename)s')
var mySprite = game.add.sprite(%(width)d, %(height)d, 'mySpriteNickname');
mySprite.animations.add('myAnimationNickname');
mySprite.animations.play();
""" % {'filename': out_filename, 'width': width, 'height': height}

class FileNotFoundError(Exception):
    pass

def open_file_or_url(url):
    try:
        return StringIO(open(url).read())
    except:
        try:
            return StringIO(requests.get(url).content)
        except:
            raise
            raise FileNotFoundError

if __name__ == '__main__':
    try:
        gif_to_sprites()
    except FileNotFoundError:
        print "Error: file not found"
