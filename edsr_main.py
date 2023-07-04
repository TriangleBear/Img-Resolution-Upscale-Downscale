import cv2
from cv2 import dnn_superres

# EDSR
# initialize super resolution object
sr = dnn_superres.DnnSuperResImpl_create()
# read the model
path = './models/EDSR_x4.pb'
sr.readModel(path)
# set the model and scale
sr.setModel('edsr', 4)
# load the image
image = cv2.imread('./images/DIV2K_valid_LR_x8/0817x8.png')
# upsample the image
upscaled = sr.upsample(image)
# save the upscaled image
cv2.imwrite('./images/output/edsr_upscaled_test_4x.png', upscaled)

# traditional method - bicubic
bicubic = cv2.resize(image, (upscaled.shape[1], upscaled.shape[0]), interpolation=cv2.INTER_CUBIC)
# save the image
cv2.imwrite('./images/output/bicubic_test_4x.png', bicubic)

