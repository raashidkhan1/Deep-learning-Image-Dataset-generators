import cv2
import numpy as np
import os

image= "C:\\Users\\Raashid\\Thesis\\Data\\KinectData\\depth_image_1.png"

img_depth = cv2.imread(image,-1)
depth_array = np.array(img_depth, dtype=np.float32)
frame = cv2.normalize(depth_array, depth_array, 0, 1, cv2.NORM_MINMAX)
cv2.imwrite('capture_depth.png',frame*255)