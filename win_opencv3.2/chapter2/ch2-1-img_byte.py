import cv2
import numpy
import os

# os.urandom 以字节为单位生成随机数
randomByteArray = bytearray(os.urandom(120000))
flatNumpyArray = numpy.array(randomByteArray)


grayImage = flatNumpyArray.reshape(300, 400)
cv2.imwrite('RandomGray.png', grayImage)
cv2.namedWindow("image_win1")
cv2.imshow("image_win1", grayImage)


bgrImage = flatNumpyArray.reshape(100, 400, 3)
print(bgrImage)
cv2.imwrite('RandomColor.png', bgrImage)
cv2.namedWindow("image_win2")
cv2.imshow("image_win2", bgrImage)

cv2.waitKey(0)
cv2.destroyAllWindows()