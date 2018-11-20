from PIL import Image
import pickle
import os.path
import random

def crop(img_path, outdir, l, area, degree):
    w, h = (300, 300)
    im = Image.open(img_path).rotate(degree, expand=True)
    x, y = im.size
    x_min, y_min, x_max, y_max = area
    for count in range(l):
        while True:
            x0 = random.randrange(x_min, x_max)
            y0 = random.randrange(y_min, y_max)
            x1 = x0 + w
            y1 = y0 + h
            print((x0,y0,x1,y1))
            if (x1 < x) & (y1 < y):
                break
        im_c = im.crop((x0, y0, x1, y1))
        head, bat_name = os.path.split(img_path)
        name, ext = os.path.splitext(bat_name)
        outpath = outdir + name + '_' + str(count) + ext
        im_c.save(outpath)
