import cv2
import numpy as np
import os


bb_image = cv2.imread("../images/hamper.jpeg")
cv2.namedWindow("testwin")
cv2.imshow("testwin", bb_image)


channel_R = np.zeros((bb_image.shape[0], bb_image.shape[1]), dtype=bb_image.dtype)
channel_G = np.zeros([bb_image.shape[0], bb_image.shape[1]], dtype=bb_image.dtype)
channel_B = np.zeros([bb_image.shape[0], bb_image.shape[1]], dtype=bb_image.dtype)

channel_B[:, :] = bb_image[:, :, 0]
channel_G[:, :] = bb_image[:, :, 1]
channel_R[:, :] = bb_image[:, :, 2]

cv2.namedWindow("win_b")
cv2.imshow("win_b", channel_B)

cv2.namedWindow("win_g")
cv2.imshow("win_g", channel_G)

cv2.namedWindow("win_r")
cv2.imshow("win_r", channel_R)

# creat 2d array
# channel_b = np.zeros()
cv2.waitKey(0)
cv2.destroyAllWindows()