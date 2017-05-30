import cv2

img = cv2.imread("../images/hamper.jpeg")

cv2.imshow("test", img)

print(img.shape)

cv2.waitKey(0)

cv2.destroyAllWindows()
