import cv2
from cv2 import dnn_superres

def upscale(image_object):
    # EDSR
    # initialize super resolution object
    sr = dnn_superres.DnnSuperResImpl_create()

    path = './models/EDSR_x4.pb'
    sr.readModel(path)

    sr.setModel('edsr', 4)

    # upsample the image
    image_object = sr.upsample(image_object)
    return image_object


