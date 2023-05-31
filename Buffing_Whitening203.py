"""
创建时间：2023年5月30日
作者：黄小芳
功能：对人像图像进行磨皮和美白处理
"""
import cv2
import dlib
import numpy as np

"""
功能：实现磨皮
输入：image是需要操作的图像，d是在滤波时选取的空间距离参数，
sigmaColor是滤波处理时选取的颜色差值范围，该值决定了周围哪些像素点能够参与到滤波中来
sigmaSpace是坐标空间中的sigma值。它的值越大，说明有越多的点能够参与到滤波计算中来
"""


# 获取椭圆肤色模型
def YCrCb_ellipse_model(image):
    skinCrCbHist = np.zeros((256, 256), dtype=np.uint8)
    cv2.ellipse(skinCrCbHist, (113, 155), (23, 24), 43, 0, 360, (255, 255, 255), -1)  # 绘制椭圆弧线
    YCrCb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)  # 转换至YCrCb空间
    (Y, Cr, Cb) = cv2.split(YCrCb)  # 拆分出Y，Cr，Cb的值
    skin = np.zeros(Cr.shape, dtype=np.uint8)  # 掩膜
    (x, y) = Cr.shape
    for i in range(0, x):
        for j in range(0, y):
            cr = YCrCb[i, j, 1]
            cb = YCrCb[i, j, 2]
            if skinCrCbHist[cr, cb] > 0:  # 若不在椭圆区间中
                skin[i][j] = 255
    res = cv2.bitwise_and(image, image, mask=skin)  # 利用位运算将滤波后的图像与原图结合，保护背景
    return skin, res  # 返回掩膜和获取只有肤色的图像


# 磨皮
def buffing(image, d, sigmaColor, sigmaSpace):
    skin, res = YCrCb_ellipse_model(image)  # 获取皮肤的掩膜数组
    kernel = np.ones((3, 3), dtype=np.uint8)
    # 对掩膜数组进行开运算，消除细小区域
    skin = cv2.erode(skin, kernel=kernel)  # 对掩膜数组进行腐蚀运算
    skin = cv2.dilate(skin, kernel=kernel)  # 对掩膜数组进行膨胀运算
    # 对图像进行双边滤波过滤
    output = cv2.bilateralFilter(image, d, sigmaColor, sigmaSpace)
    output = np.array(output, dtype=np.uint8)
    output = cv2.bitwise_and(output, output, mask=skin)  # 将皮肤与背景分离
    skin = cv2.bitwise_not(skin)
    output = cv2.add(output, cv2.bitwise_and(image, image, mask=skin))  # 磨皮后的结果与背景叠加
    return output


# 获取特征点检测器
dlib_path = './shape_predictor_81_face_landmarks.dat'

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(dlib_path)

jaw_point = list(range(0, 17)) + list(range(68, 81))  # 获取额头特征点坐标
left_eye = list(range(42, 48))  # 获取左眼特征点坐标
right_eye = list(range(36, 42))  # 获取右眼特征点坐标
left_brow = list(range(22, 27))
right_brow = list(range(17, 22))
mouth = list(range(48, 61))  # 获取嘴巴特征点坐标
nose = list(range(27, 35))


# 获取81个特征点
def get_landmark(img):
    faces = detector(img, 1)
    shape = predictor(img, faces[0]).parts()
    return np.matrix([[p.x, p.y] for p in shape])


# 根据坐标点画凸包
def draw_convex_hull(img, points, color):
    hull = cv2.convexHull(points)
    cv2.fillConvexPoly(img, hull, color=color)


# 获取只含面部的凸包图片
def get_skin_mask(img):
    landmarks = get_landmark(img)  # 获取特征点坐标
    mask = np.zeros(img.shape[:2])
    draw_convex_hull(mask, landmarks[jaw_point], color=1)  # 画出面部的凸包
    for index in [mouth, left_eye, right_eye]:  # 去除眼睛、嘴巴和眉毛的轮廓
        draw_convex_hull(mask, landmarks[index], color=0)
    mask = np.array([mask] * 3).transpose(1, 2, 0)  # 将矩阵进行转置
    return mask


# 美白
def whitening(image, value):
    img_skin = get_skin_mask(image)  # 获取面部轮廓
    midtones_add = np.zeros(256)
    # 获取色调基本模板
    for i in range(256):
        midtones_add[i] = 0.667 * (1 - ((i - 127) / 127) * ((i - 127) / 127))
    lookup = np.zeros(256, dtype='uint8')
    # 对图像像素进行调整
    for i in range(256):
        red = i
        red += np.uint8(value * midtones_add[red])
        red = max(0, red)
        lookup[i] = np.uint(red)

    # 将原图像的人脸部分进行调整
    w, h, c = image.shape
    for i in range(w):
        for j in range(h):
            if img_skin[i, j, 0] == 1:
                image[i, j, 0] = lookup[image[i, j, 0]]
                image[i, j, 1] = lookup[image[i, j, 1]]
                image[i, j, 2] = lookup[image[i, j, 2]]
    return image
