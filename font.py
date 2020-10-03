import os
from pprint import pprint
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from fontTools import ttLib, pens
import fontTools
# from fontTools.pens import reportLabPen

size = 480
text = ""
font='D:/r/kode/font explorer/HACK REGULAR NERD FONT COMPLETE MONO WINDOWS COMPATIBLE.TTF'

def get_dict_gname_guni(fontFile):
    with ttLib.TTFont(fontFile) as font:
        cmap = {v: k for k, v in font.getBestCmap().items()}
        return cmap
def get_font_name(fontFile):
    with ttLib.TTFont(fontFile) as font:
        # pprint(font["name"].getName())
        for record in font['name'].names:
            if record.nameID == 4:
                return record.string.decode("utf-8")
            elif record.nameID == 1:
                return record.string.decode("utf-8")
            else:
                file = os.path.split(fontFile)[1]
                return os.path.splitext(file)[0]
def get_font_description(fontFile):
    with ttLib.TTFont(fontFile) as font:
        # pprint(font["name"].getName())
        for record in font['name'].names:
            if record.nameID == 10:
                return record.string.decode("utf-8")
        return ""


def dowloadGlyph(size,text,font,name):
    image = Image.new("RGBA", (size*2, size*2), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font, size)
    w, h = draw.textsize(text, font=font)
    draw.text(((size*2 - w) / 2, (size*2 - h)/2), text, fill="black",font=font)
    image.save(name + ".png")

if __name__ == "__main__":
    get_font_name(font)