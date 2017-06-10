from aip import AipFace
import cv2

# 定义常量
APP_ID = '9749855'
API_KEY = 'ewaPhQ2wRjH2F2ykfTp1K38j'
SECRET_KEY = 'tn5x76y0a8OGX2w3N2d66QzdprGisGzB'

# 初始化AipFace对象
aipFace = AipFace(APP_ID, API_KEY, SECRET_KEY)
# 定义参数变量
options = {
    'max_face_num': 10,
    'face_fields': "age",
}


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 调用人脸属性检测接口
result = aipFace.detect(get_file_content('../../images/xichang.jpg'), options)
img = cv2.imread('../../images/xichang.jpg')
cv2.imshow('11', img)
# print("number of faces:" + str(result['result_num']))
print("total result:")
for key, value in result.items():
    print(key, '-->', value)

print("detail result:")
for key, value in result['result'][0].items():
    print(key, '-->', value)
cv2.waitKey(0)
cv2.destroyAllWindows()
