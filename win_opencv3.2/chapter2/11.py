import cv2
import numpy as np

# 使用Numpy 数组来实现图像通道分离
# img = cv2.imread("../images/hamper.jpeg")

img = cv2.imread("./timg.jpg")
# b, g, r = cv2.split(img)
# cv2.imshow("Blue", r)
# cv2.imshow("Red", g)
# cv2.imshow("Green", b)

# 创建3个跟图像一样大小的矩阵，数值全部为0
b = np.zeros((img.shape[0], img.shape[1]), dtype=img.dtype)
g = np.zeros((img.shape[0], img.shape[1]), dtype=img.dtype)
r = np.zeros((img.shape[0], img.shape[1]), dtype=img.dtype)

# 复制图像通道里的数据
b[:, :] = img[:, :, 0]  # 复制 b 通道的数据
g[:, :] = img[:, :, 1]  # 复制 g 通道的数据
r[:, :] = img[:, :, 2]  # 复制 r 通道的数据

cv2.imshow("Blue", b)
cv2.imshow("Red", r)
cv2.imshow("Green", g)
cv2.waitKey(0)
cv2.destroyAllWindows()