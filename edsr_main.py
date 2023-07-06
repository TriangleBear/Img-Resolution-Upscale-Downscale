import cv2
from cv2 import dnn_superres
from PIL import Image
import base64
from base64 import decodestring

#(width,height)

def edsr(uploadedImage):
    js_image = Image.fromstring('RGB', decodestring(uploadedImage))

    sr = dnn_superres.DnnSuperResImpl_create()

    path = './models/EDSR_x4.pb'
    sr.readModel(path)

    sr.setModel('edsr', 4)

    py_image = cv2.imread(js_image)

    py_upscaled = sr.upsample(py_image)

    #with open(py_upscaled, "rb") as py_convert:
        #js_upscaled = base64.b64encode(py_convert.read())

    return py_upscaled

    #cv2.imwrite('./images/output/edsr_upscaled_test_4x.png', py_upscaled)


