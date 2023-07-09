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





<<<<<<< HEAD
=======
# traditional method - bicubic
bicubic = cv2.resize(image, (upscaled.shape[1], upscaled.shape[0]), interpolation=cv2.INTER_CUBIC)
# save the image
cv2.imwrite('./images/output/bicubic_test_4x.png', bicubic)

>>>>>>> parent of b18fc28 (Default)
