import cv2
import numpy as np

# 使用Numpy 数组来实现图像通道分离
# img = cv2.imread("../images/hamper.jpeg")

img = cv2.imread("../images/color_wave.jpg")

# change the channel num to see pic change
img[:, :, 2] = 0


cv2.imshow("Blue", img)

cv2.waitKey(0)
cv2.destroyAllWindows()