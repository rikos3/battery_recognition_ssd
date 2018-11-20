from PIL import Image
import pickle
import os.path
import random

def crop_300(coordinates, ssdDir, outdir, l):
    w, h = (300, 300)
    coordinates2 = []
    for img_path, lst, klst, degree in coordinates:
        i = 0
        head, bat_name = os.path.split(img_path)
        head, bat_dir = os.path.split(head)
        head, im_dir = os.path.split(head)
        bat_dir += '/'
        im_dir += '/'
        path = ssdDir + im_dir + bat_dir + bat_name
        im = Image.open(path).rotate(degree, expand=True)
        x, y = im.size
        for top, left, bottom, right in lst:
            for count in range(l):
                while True:
                    x0 = random.randrange(0, x - w)
                    y0 = random.randrange(0, y - h)
                    x1 = x0 + w
                    y1 = y0 + h
                    if (x0 < top) & (y0 < left) & (x1 > bottom) & (y1 > right):
                        break
                im_c = im.crop((x0, y0, x1, y1))
                name, ext = os.path.splitext(bat_name)
                outpath = outdir + name + '_' + str(i) + '_' + str(count) + ext
                im_c.save(outpath)
                Image.open(outpath)
                lst2 = []
                klst2 = []
                for j in range(len(lst)):
                    top, left, bottom, right = lst[j]
                    new_top = top - x0
                    new_left = left - y0
                    new_bottom = bottom - x0
                    new_right = right - y0
                    if (new_top > 0) & (new_left > 0) & (new_bottom < w) & (new_right < h):
                        lst2.append((new_top, new_left, new_bottom, new_right))
                        klst2.append(klst[j])
                coordinates2.append((outpath, lst2, klst2, degree))
        i += 1
    return coordinates2
