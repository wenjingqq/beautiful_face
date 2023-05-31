# 调整饱和度
import cv2
import numpy as np


def saturation(image, value):
    img_hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    if value > 2:
        img_hls[:, :, 2] = np.log(img_hls[:, :, 2] / 255 * (value - 1) + 1) / np.log(value + 1) * 255
    if value < 0:
        img_hls[:, :, 2] = np.uint8(img_hls[:, :, 2] / np.log(- value + np.e))
    image = cv2.cvtColor(img_hls, cv2.COLOR_HLS2BGR)
    return image


# 明度调节
def darker(image, value):
    img_hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)  # 将图片转为hls空间
    # 选取L通道调节亮度
    # 调亮，进行指数调整
    if value > 3:
        img_hls[:, :, 1] = np.log(img_hls[:, :, 1] / 255 * (value - 1) + 1) / np.log(value + 1) * 255
    # 调暗，进行线性调整
    if value < 0:
        img_hls[:, :, 1] = np.uint8(img_hls[:, :, 1] / np.log(- value + np.e))
    output = cv2.cvtColor(img_hls, cv2.COLOR_HLS2BGR)  # 转为BGR
    return output


if __name__ == '__main__':
    image = cv2.imread('C:\\Users\\KeKe\\Pictures\\pic_2023-05-31-16-12-25.jpg')
    cv2.imshow('image', image)
    out1 = saturation(image, 5)
    out2 = darker(image, 6)
    cv2.imshow('output', out1)
    cv2.imshow('output2', out2)
    cv2.waitKey(0)
