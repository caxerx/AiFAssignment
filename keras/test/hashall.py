from PIL import Image
import imagehash
import os

DIR = "../data/combined"


def get_extension(format):
    if format == 'JPEG':
        return "jpg"
    if format == 'PNG':
        return "png"
    return "DUNNO"


for folder in os.listdir(DIR):
    for img in os.listdir(DIR + "/" + folder):
        img_path = DIR + "/" + folder + "/" + img
        pimg = Image.open(img_path)
        hash = imagehash.average_hash(pimg)
        try:
            os.rename(img_path, DIR + "/" + folder + "/" + str(hash) + "." + get_extension(pimg.format))
        except FileExistsError:
            os.remove(img_path)
