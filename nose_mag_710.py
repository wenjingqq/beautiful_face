
import math
import cv2
import imutils
import numpy as np
import dlib


def get_face_key_point_710(img_src, detector, predictor):
    # 将图像转换为灰度图
    # 转灰度时图片要为三通道
    img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)

    # 存储检测到的人脸关键点
    store_key = []

    # 在灰度框中检测人脸，得到人脸检测矩形框4点坐标
    rects = detector(img_gray, 0)

    # 遍历每一个检测到的人脸
    for i in range(len(rects)):
        # 获取当前人脸的关键点
        # np.matrix:返回矩阵
        land_marks_node = np.matrix([[p.x, p.y] for p in predictor(img_gray, rects[i]).parts()])
        # 将关键点存储在结果中
        store_key.append(land_marks_node)

    return store_key

# 变化前u附近的值求出u的像素值
def BilinearInsert_710(ori_img, ux, uy):
    # 双线性插值法
    w, h, c = ori_img.shape

    if c == 3:
        # 通道数为3，是彩色图像
        x1 = int(ux)
        x2 = x1+1
        y1 = int(uy)
        y2 = y1+1

        # 计算插值的四个部分
        part1 = ori_img[y1, x1].astype(float)*(float(x2)-ux)*(float(y2)-uy)
        part2 = ori_img[y1, x2].astype(float)*(ux-float(x1))*(float(y2)-uy)
        part3 = ori_img[y2, x1].astype(float)*(float(x2) - ux)*(uy-float(y1))
        part4 = ori_img[y2, x2].astype(float)*(ux-float(x1))*(uy - float(y1))

        # 得到插值结果
        insertValue = part1+part2+part3+part4

        return insertValue.astype(np.int8)


# 利用局部缩小变形实现鼻子的缩小
#  r:缩小的距离   c:鼻子上的点，start表示
def local_scaling_710(origin_img, start_x, start_y, radius, a):
    r_2 = float(radius*radius)
    resu_image = origin_img.copy()

    H, W, C = origin_img.shape

    # 遍历每一个点x(i,j)
    for i in range(W):
        for j in range(H):
            # 该点是否在矩形范围内
            # 以c为中心的2r * 2r的矩阵，矩形里有以c为圆心半径为r的内切圆
            if math.fabs(i-start_x) > radius and math.fabs(j-start_y) > radius:
                continue

            # distance = |x-c|^2
            distance = math.pow((i - start_x), 2) + math.pow((j - start_y), 2)

            # 该点是否在形变圆内
            if(distance < r_2):
                # 计算公式中括号里的部分
                # kuo = (1- ( |x-c|/r -1 )^2 *a)
                chu = math.sqrt(distance) / radius
                kuo = 1 - math.pow((chu - 1), 2) * a

                # 映射原位置
                # 计算x点（i,j）的原坐标u
                ux = start_x + kuo * (i - start_x)  # x-c= i - start_x
                uy = start_y + kuo * (j - start_y)

                # 根据双线性插值法得到ux, uy的像素值
                value = BilinearInsert_710(origin_img, ux, uy)
                # 改变当前 i ，j的值
                resu_image[j, i] = value

    return resu_image


# 对于鼻子的处理
def core_nose_710(image, detector, predictor, degree):
    if degree <= 55:
        i = 1
    elif 55 < degree <= 100:
        i = 0

    degree = 0.01 * degree * -1

    # Parm1：左变鼻子的一个关键点
    # 左右两边的两个点分别取自一个在鼻子上，一个在鼻梁上
    parm1 = [31, 32]
    parm2 = [30, 30]
    parm3 = [35, 34]
    parm4 = [30, 30]
    # i = 1

    # 获得多个人脸的关键点
    landmarks = get_face_key_point_710(image, detector, predictor)

    # 如果未检测到人脸关键点，就不进行功能
    if len(landmarks) == 0:
        return image

    # 遍历每一个人脸关键点
    for landmarks_node in landmarks:
        # 获取左边的两个关键点
        left_nose_p1 = landmarks_node[parm1[i]]
        left_nose_p2 = landmarks_node[parm2[i]]

        # 获取右边的两个关键点
        right_nose_p1 = landmarks_node[parm3[i]]
        right_nose_p2 = landmarks_node[parm4[i]]

        # 获取鼻尖的关键点，第31个点
        nose_p = landmarks_node[30]

        # 右边两个点的距离作为右边鼻子缩小的距离
        # √ ((x1-x2)^2+ (y1-y2)^2)
        r_left = math.sqrt(math.pow((left_nose_p1[0, 0] - left_nose_p2[0, 0]), 2) +
                           math.pow((left_nose_p1[0, 1] - left_nose_p2[0, 1]), 2))

        # 左边两个点的距离作为左边鼻子缩小的距离
        r_right = math.sqrt(math.pow((right_nose_p1[0, 0] - right_nose_p2[0, 0]), 2) +
                            math.pow((right_nose_p1[0, 1] - right_nose_p2[0, 1]), 2))

        # 缩小左边
        result_image = local_scaling_710(image, left_nose_p1[0, 0], left_nose_p1[0, 1],r_left, degree)

        # 缩小右边
        result_image = local_scaling_710(result_image, right_nose_p1[0, 0], right_nose_p1[0, 1], r_right, degree)

        # 返回处理后的图像
        return result_image

# 对图片进行缩小鼻子的处理
def picture_nose_710(im, degree):

    # 将图像的宽度调整为600像素
    image = imutils.resize(im, width=600)

    # 获得脸部位置检测器
    detector = dlib.get_frontal_face_detector()
    # Dlib 人脸 landmark 特征点检测器
    predictor = dlib.shape_predictor('data/shape_predictor_68_face_landmarks.dat')

    result = core_nose_710(image, detector, predictor, degree)
    return result


if __name__ == '__main__':
    degree = 30
    path_img = 'E:/ashijue/myself.jpg'  #   test_face_lift.jpg
    img = cv2.imread(path_img)
    img = imutils.resize(img, width=600)
    cv2.imshow('or', img)

    result = picture_nose_710(img, degree)
    cv2.imshow('result', result)
    cv2.waitKey(0)

