import cv2
from cv2 import dnn_superres

def edsr(uploadedImage):
    sr = dnn_superres.DnnSuperResImpl_create()
    path = './models/EDSR_x4.pb'
    sr.readModel(path)
    sr.setModel('edsr', 4)
    image = cv2.imread(uploadedImage)
    upscaled = sr.upsample(image)
    return upscaled