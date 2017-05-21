import cv2
import numpy
import os


randomByteArray = bytearray(os.urandom(12))
flatNumpyArray = numpy.array(randomByteArray)
# print(flatNumpyArray)

image = flatNumpyArray.reshape(2, 2, 3)
print("image")
print(image)
print("image[0, 0]:")
print(image[0, 0])

# cv2.namedWindow("testwin")
cv2.imshow("testwin", image)
cv2.waitKey(0)
cv2.destroyAllWindows()