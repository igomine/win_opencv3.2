import cv2

img = cv2.imread("../images/color_wave.jpg")
cv2.imshow("origin", img)

# change the channel num to see pic change
img[:, :, 2] = 0

cv2.imshow("del_red", img)

cv2.waitKey(0)
cv2.destroyAllWindows()