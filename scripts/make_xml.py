import pickle
import os.path
import numpy as np
from PIL import Image
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import os
import os.path

def Make_XML(traindata, outdir, keyword):
    coordinates = pickle.load(open(traindata, "rb"))

    for line in coordinates:
        im_path, lst, klst, degree = line
        im = Image.open(im_path).rotate(degree, expand=True)
        dir_name, file_name = os.path.split(im_path)
        w, h = im.size

        value_w = str(w)
        value_h = str(h)
        value_d = '3'

        root = ET.Element('annotation')

        folder = ET.SubElement(root, 'folder')
        folder.text = dir_name

        file = ET.SubElement(root, 'filename')
        file.text = file_name

        size = ET.SubElement(root, 'size')
        width = ET.SubElement(size, 'width')
        width.text = value_w
        height = ET.SubElement(size, 'height')
        height.text = value_h
        depth = ET.SubElement(size, 'depth')
        depth.text = value_d
        
        for i in range(len(lst)):
            top, left, bottom, right = lst[i]

            object = ET.SubElement(root, 'object')
            name = ET.SubElement(object, 'name')
            if keyword == True:
                name.text = klst[i]
            else:
                name.text = "keyword"
            bndbox = ET.SubElement(object, 'bndbox')
            xmin = ET.SubElement(bndbox, 'xmin')
            xmin.text = str(top)
            ymin = ET.SubElement(bndbox, 'ymin')
            ymin.text = str(left)
            xmax = ET.SubElement(bndbox, 'xmax')
            xmax.text = str(bottom)
            ymax = ET.SubElement(bndbox, 'ymax')
            ymax.text = str(right)

        string = ET.tostring(root, 'utf-8')
        pretty_string = minidom.parseString(string).toprettyxml(indent= '  ')

        key, ext = os.path.splitext(file_name)

        outpath = outdir + key + '.xml'
        with open(outpath, 'w') as f:
            f.write(pretty_string)

def Make_XML2(traindata, outdir, keyword):
    coordinates = pickle.load(open(traindata, "rb"))

    for line in coordinates:
        im_path, lst, klst, degree = line
        im = Image.open(im_path).rotate(degree, expand=True)
        dir_name, file_name = os.path.split(im_path)
        w, h = im.size

        value_w = str(w)
        value_h = str(h)
        value_d = '3'

        root = ET.Element('annotation')

        folder = ET.SubElement(root, 'folder')
        folder.text = dir_name

        file = ET.SubElement(root, 'filename')
        file.text = file_name

        size = ET.SubElement(root, 'size')
        width = ET.SubElement(size, 'width')
        width.text = value_w
        height = ET.SubElement(size, 'height')
        height.text = value_h
        depth = ET.SubElement(size, 'depth')
        depth.text = value_d
        
        rad = np.deg2rad(degree)

        for i in range(len(lst)):
            top, left, bottom, right = lst[i]

            w0 = abs(bottom - top)
            h0 = abs(right - left)
            w_2 = w / 2
            h_2 = h / 2

            A = np.array([[np.cos(rad),-np.sin(rad)],[np.sin(rad),np.cos(rad)]])
            B = np.array([w_2,h_2])
            X_min = np.array([top,left])
            X_max = np.array([bottom,right])

            C = np.array([np.dot(A,X_min-B)+B, np.dot(A,X_max-B)+B]).T
            X = np.sort(C[0])
            Y = np.sort(C[1])

            object = ET.SubElement(root, 'object')
            name = ET.SubElement(object, 'name')
            if keyword == True:
                name.text = klst[i]
            else:
                name.text = "keyword"
            bndbox = ET.SubElement(object, 'bndbox')
            xmin = ET.SubElement(bndbox, 'xmin')
            xmin.text = str(X[0])
            ymin = ET.SubElement(bndbox, 'ymin')
            ymin.text = str(Y[0])
            xmax = ET.SubElement(bndbox, 'xmax')
            xmax.text = str(X[1])
            ymax = ET.SubElement(bndbox, 'ymax')
            ymax.text = str(Y[1])

        string = ET.tostring(root, 'utf-8')
        pretty_string = minidom.parseString(string).toprettyxml(indent= '  ')

        key, ext = os.path.splitext(file_name)

        outpath = outdir + key + '.xml'
        with open(outpath, 'w') as f:
            f.write(pretty_string)
