import os
import sys
import time

import numpy as np
import qtawesome
from PyQt5.QtCore import QSize, QDir, QTimer, Qt
from PyQt5.QtGui import QPainter, QPixmap, QImage
from PyQt5.QtWidgets import QFileDialog, QMessageBox

import Buffing_Whitening203
from MainWindow203 import *
from PictureWindow203 import *
from VideoWindow203 import *
from CameraWindow203 import *
from Buffing_Whitening203 import *


class myMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(myMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.beautify_window()  # 美化界面

        self.camera_window = None
        self.video_window = None  # 视频美容的窗口信号
        self.picture_window = None  # 人像美容的窗口信号

        # 关联触发事件
        self.pushButton.clicked.connect(self.picture_win)  # 打开人像美容界面
        self.pushButton_2.clicked.connect(self.video_win)  # 打开视频美容界面
        self.pushButton_3.clicked.connect(self.camera_win)  # 打开相机

    # 美化界面
    def beautify_window(self):
        self.resize(900, 850)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setIconSize(QSize(40, 40))
        window_icon = qtawesome.icon('fa5b.optin-monster', color='pink')  # 添加窗口图标
        self.setWindowIcon(window_icon)
        camera_icon = qtawesome.icon('fa5s.camera', color='pink')  # 添加相机图标
        self.pushButton_3.setIcon(camera_icon)
        self.pushButton_3.setIconSize(QSize(60, 60))
        picture_icon = qtawesome.icon('mdi.face-woman-shimmer', color='pink')  # 添加人像美容图标
        self.pushButton.setIcon(picture_icon)
        self.pushButton.setIconSize(QSize(60, 60))
        video_icon = qtawesome.icon('mdi.video-vintage', color='pink')  # 添加视频美容图标
        self.pushButton_2.setIcon(video_icon)
        self.pushButton_2.setIconSize(QSize(60, 60))
        help_icon = qtawesome.icon('fa5s.question', color='yellow')  # 添加帮助图标
        self.actionbanzhu.setIcon(help_icon)
        delete_icon = qtawesome.icon('ri.delete-bin-line', color='white')  # 添加删除图标
        self.actionshanchu.setIcon(delete_icon)
        save_icon = qtawesome.icon('ri.save-3-line', color='white')  # 添加保存图标
        self.actionbaocun.setIcon(save_icon)

    # 添加背景图片
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawRect(self.rect())
        painter.setOpacity(0.9)
        pixmap = QPixmap("./background2.jpg")  # 换成自己的图片的相对路径
        painter.drawPixmap(self.rect(), pixmap)

    # 打开人像美容界面
    def picture_win(self):
        self.close()
        self.picture_window = myPictureWindow()
        self.picture_window.show()

    # 打开视频美容界面
    def video_win(self):
        self.close()
        self.video_window = myVideoWindow()
        self.video_window.show()

    # 打开相机界面
    def camera_win(self):
        self.close()
        self.camera_window = myCameraWindow()
        self.camera_window.show()


# 人像美容界面
class myPictureWindow(QtWidgets.QMainWindow, PictureWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.d = 15
        self.mainWindow = None
        self.setupUi(self)
        self.beautify_window()  # 美化界面
        self.relevancy()  # 关联事件
        self.current_path = None

    # 美化界面
    def beautify_window(self):
        # 人像美容界面美化
        self.resize(900, 850)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setIconSize(QSize(40, 40))
        win_icon = qtawesome.icon('fa5b.optin-monster', color='pink')  # 设置窗口图标
        self.setWindowIcon(win_icon)
        open_icon = qtawesome.icon('ri.folder-open-line', color='lightblue')  # 设置打开图标
        self.actionopen.setIcon(open_icon)
        delete_icon = qtawesome.icon('ri.delete-bin-line', color='lightblue')  # 设置删除图标
        self.actiondelete.setIcon(delete_icon)
        save_icon = qtawesome.icon('ri.save-3-line', color='lightblue')  # 设置保存图标
        self.actionsave.setIcon(save_icon)
        mopi_icon = qtawesome.icon('ph.circle-half-bold', color='white')  # 设置磨皮图标
        self.mopi_pushButton.setIcon(mopi_icon)
        self.mopi_pushButton.setIconSize(QSize(40, 40))
        meibai_icon = qtawesome.icon('mdi6.face-woman-shimmer-outline', color='white')  # 设置美白图标
        self.meibai_pushButton.setIcon(meibai_icon)
        self.meibai_pushButton.setIconSize(QSize(40, 40))
        shoulian_icon = qtawesome.icon('ph.person-thin', color='white')  # 设置瘦脸图标
        self.shoulian_pushButton.setIcon(shoulian_icon)
        self.shoulian_pushButton.setIconSize(QSize(40, 40))
        mouth_icon = qtawesome.icon('mdi6.lipstick', color='white')  # 设置红唇图标
        self.mouth_pushButton.setIcon(mouth_icon)
        self.mouth_pushButton.setIconSize(QSize(40, 40))
        eye_icon = qtawesome.icon('ph.eye', color='white')  # 设置眼睛图标
        self.eye_pushButton.setIcon(eye_icon)
        self.eye_pushButton.setIconSize(QSize(40, 40))
        meimao_icon = qtawesome.icon('ph.eye-closed-bold', color='white')  # 设置眉毛图标
        self.meimao_pushButton.setIcon(meimao_icon)
        self.meimao_pushButton.setIconSize(QSize(40, 40))
        # 设置磨皮滚动条的范围、步长
        self.mopi_horizontalSlider.setMinimum(0)
        self.mopi_horizontalSlider.setMaximum(100)
        self.mopi_horizontalSlider.setSingleStep(1)
        # 设置美白滚动条的范围、步长
        self.meibai_horizontalSlider.setMinimum(0)
        self.meibai_horizontalSlider.setMaximum(40)
        self.meibai_horizontalSlider.setSingleStep(1)
        # 设置眼睛滚动条的范围、步长
        self.eye_horizontalSlider.setMinimum(0)
        self.eye_horizontalSlider.setMaximum(100)
        self.eye_horizontalSlider.setSingleStep(1)

    # 关联组件和时间
    def relevancy(self):
        self.actionopen.triggered.connect(self.get_open)  # 关联打开文件
        self.actionsave.triggered.connect(self.get_Save)  # 关联保存文件
        self.actiondelete.triggered.connect(self.get_delete)  # 关联删除文件
        self.mopi_pushButton.clicked.connect(self.get_buffing)  # 关联磨皮
        self.meibai_pushButton.clicked.connect(self.get_whitening)  # 关联美白

    # 重写关闭按钮事件，关闭本窗口，返回主窗口
    def closeEvent(self, event):
        self.mainWindow = myMainWindow()
        self.mainWindow.show()
        self.close()

    # 设置打开菜单open的触发事件
    def get_open(self):
        flag = False  # 标记图片格式是否正确
        dig = QFileDialog()  # 创建一个
        dig.setFileMode(QFileDialog.AnyFile)
        dig.setFilter(QDir.Files)
        img_type = [".bmp", ".jpg", ".png", ".gif"]
        if dig.exec_():
            filename = dig.selectedFiles()
            try:
                with open(filename[0], 'r') as file:
                    self.current_path = filename[0]
                    for ig in img_type:
                        if ig not in self.current_path:
                            continue
                        else:
                            flag = True  # 打开图片格式正确
                            # 获取图片并自适应窗口大小
                            img = QPixmap(filename[0]).scaled(self.picture_label.width(), self.picture_label.height())
                            self.picture_label.setPixmap(img)
                            self.picture_label.setScaledContents(True)
                    file.close()
                    if not flag:
                        QMessageBox.information(self, "警告", "暂不支持此格式文件！", QMessageBox.Ok)
            except Exception:
                QMessageBox.critical(None, '错误', '文件打开失败', QMessageBox.Ok)

    # 为保存菜单创建关联事件
    def get_Save(self):
        data = self.picture_label.pixmap().toImage()
        fpath, ftype = QFileDialog.getSaveFileName(self, '保存图片', ".\\", "*.jpg;;*.png;;*.bmp;;*.gif;;All Files(*)")
        self.current_path = fpath
        data.save(fpath)

    # 为删除菜单创建关联事件
    def get_delete(self):
        select = QMessageBox.information(None, '删除', '是否确定删除该文件？', QMessageBox.Yes | QMessageBox.No)
        if select == QMessageBox.Yes:
            self.picture_label.clear()
            os.remove(self.current_path)

    def qimage2mat(self, qimg):
        ptr = qimg.constBits()
        ptr.setsize(qimg.byteCount())
        mat = np.array(ptr).reshape(qimg.height(), qimg.width(), 4)  # 注意这地方通道数一定要填4，否则出错
        return mat

    # 磨皮
    def get_buffing(self):
        # arr = np.fromfile(self.current_path, dtype=np.uint8)
        # image = cv2.imdecode(arr, cv2.IMREAD_COLOR)  # 读取当前图片
        image = self.picture_label.pixmap().toImage()  # 获取界面展示图片
        image = self.qimage2mat(image)  # 将QImage图片转为MAT（BGRA）图片
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)  # 将BGRA图片转为BGR图片
        output = Buffing_Whitening203.buffing(image, self.d, self.mopi_horizontalSlider.value(),
                                              self.mopi_horizontalSlider.value())
        img = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)  # 将图像转为灰度图像
        # 视频流的长和宽
        height, width = img.shape[:2]
        pixmap = QImage(img.data, width, height,width*3, QImage.Format_RGB888)
        # 自适应窗口大小
        pixmap = QPixmap.fromImage(pixmap).scaled(self.picture_label.width(), self.picture_label.height())
        self.picture_label.setPixmap(pixmap)
        self.picture_label.setScaledContents(True)

    # 美白
    def get_whitening(self):
        # arr = np.fromfile(self.current_path, dtype=np.uint8)
        # image = cv2.imdecode(arr, cv2.IMREAD_COLOR)  # 读取当前图片
        image = self.picture_label.pixmap().toImage()  # 获取界面展示图片
        image = self.qimage2mat(image)  # 将QImage图片转为MAT（BGRA）图片
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)  # 将BGRA图片转为BGR图片
        output = Buffing_Whitening203.whitening(image,self.meibai_horizontalSlider.value())  # 对图片进行美白
        img = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)  # 将图像转为灰度图像
        # 视频流的长和宽
        height, width = img.shape[:2]
        pixmap = QImage(img.data, width, height, width*3, QImage.Format_RGB888)
        # 自适应窗口大小
        pixmap = QPixmap.fromImage(pixmap).scaled(self.picture_label.width(), self.picture_label.height())
        self.picture_label.setPixmap(pixmap)
        self.picture_label.setScaledContents(True)


# 视频美容界面
class myVideoWindow(QtWidgets.QMainWindow, VideoWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.beautify_window()  # 美化界面
        self.num = 1  # 用于记录视频是处于播放还是暂停状态
        self.playing = None
        self.timer = None
        self.mainWindow = None
        self.current_path = None
        self.mopi_flag = False
        self.meibai_flag = False
        self.shoulian_flag = False
        self.eye_flag = False
        self.mouth_flag = False
        self.video = []  # 用于存储视频

        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.d = 15

        # 初始化按钮
        self.actionstart_T.setEnabled(False)  # 初始化开始播放视频按钮不可使用
        self.actiontimeout_E.setEnabled(False)  # 初始化暂停播放视频按钮不可使用
        self.actionclosevideo.setEnabled(False)  # 初始化关闭摄像头按钮不可使用

        # 打开摄像头
        self.cap = cv2.VideoCapture()
        # 初始化timer定时器
        self.init_timer()
        # 关联组件和事件
        self.relevancy()

        # 设置磨皮、美白、眼睛的滚动条范围和步长
        self.mopi_horizontalSlider.setMinimum(0)
        self.mopi_horizontalSlider.setMaximum(100)
        self.mopi_horizontalSlider.setSingleStep(1)
        self.meibai_horizontalSlider.setMinimum(0)
        self.meibai_horizontalSlider.setMaximum(40)
        self.meibai_horizontalSlider.setSingleStep(1)
        self.eye_horizontalSlider.setMinimum(0)
        self.eye_horizontalSlider.setMaximum(100)
        self.eye_horizontalSlider.setSingleStep(1)

    # 美化界面
    def beautify_window(self):
        # 视频美容界面美化
        self.resize(800, 750)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setIconSize(QSize(40, 40))
        win_icon = qtawesome.icon('fa5b.optin-monster', color='lightblue')  # 设置窗口图标
        self.setWindowIcon(win_icon)
        open_icon = qtawesome.icon('ri.folder-open-line', color='pink')  # 设置打开图标
        self.actionopen_O.setIcon(open_icon)
        delete_icon = qtawesome.icon('ri.delete-bin-line', color='pink')  # 设置删除图标
        self.actiondelete_D.setIcon(delete_icon)
        save_icon = qtawesome.icon('ri.save-3-line', color='pink')  # 设置保存图标
        self.actionsave_S.setIcon(save_icon)
        openvideo_icon = qtawesome.icon('mdi.video-check-outline', color='pink')  # 设置打开摄像头图标
        self.actionopenvideo.setIcon(openvideo_icon)
        closevideo_icon = qtawesome.icon('mdi.video-minus-outline', color='pink')  # 设置关闭摄像头图标
        self.actionclosevideo.setIcon(closevideo_icon)
        start_icon = qtawesome.icon('fa5.pause-circle', color='pink')  # 设置开始播放视频图标
        self.actionstart_T.setIcon(start_icon)
        timeout_icon = qtawesome.icon('fa5.play-circle', color='pink')  # 设置暂停播放视频图标
        self.actiontimeout_E.setIcon(timeout_icon)
        close_icon = qtawesome.icon('ei.eye-close', color='pink')  # 设置关闭视频图标
        self.actionclose_L.setIcon(close_icon)
        mopi_icon = qtawesome.icon('ph.circle-half-bold', color='pink')  # 设置磨皮图标
        self.mopi_pushButton.setIcon(mopi_icon)
        self.mopi_pushButton.setIconSize(QSize(40, 40))
        meibai_icon = qtawesome.icon('mdi6.face-woman-shimmer-outline', color='pink')  # 设置美白图标
        self.meibai_pushButton.setIcon(meibai_icon)
        self.meibai_pushButton.setIconSize(QSize(40, 40))
        shoulian_icon = qtawesome.icon('ph.person-thin', color='pink')  # 设置瘦脸图标
        self.shoulian_pushButton.setIcon(shoulian_icon)
        self.shoulian_pushButton.setIconSize(QSize(40, 40))
        mouth_icon = qtawesome.icon('mdi6.lipstick', color='pink')  # 设置红唇图标
        self.mouth_pushButton.setIcon(mouth_icon)
        self.mouth_pushButton.setIconSize(QSize(40, 40))
        eye_icon = qtawesome.icon('ph.eye', color='pink')  # 设置眼睛图标
        self.eye_pushButton.setIcon(eye_icon)
        self.eye_pushButton.setIconSize(QSize(40, 40))
        meimao_icon = qtawesome.icon('ph.eye-closed-bold', color='pink')  # 设置眉毛图标
        self.meimao_pushButton.setIcon(meimao_icon)
        self.meimao_pushButton.setIconSize(QSize(40, 40))

    # 关联事件
    def relevancy(self):
        self.actionopen_O.triggered.connect(self.get_open)
        self.actionstart_T.triggered.connect(self.play_video)
        self.actiontimeout_E.triggered.connect(self.play_video)
        self.actionclose_L.triggered.connect(self.close_video)
        self.actionopenvideo.triggered.connect(self.open_camera)
        self.actionclosevideo.triggered.connect(self.close_camera)
        self.actionsave_S.triggered.connect(self.get_save)

    # 重写关闭按钮事件，关闭本窗口，返回主窗口
    def closeEvent(self, event):
        self.mainWindow = myMainWindow()
        self.mainWindow.show()
        self.close()

    # 保存视频
    def get_save(self):
        now_time = fr"video{time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))}"  # 获取拍摄时间
        if not os.path.exists('.\\picture'):
            os.makedirs('.\\picture')
        width, height = self.video[0].shape[:2]
        out = cv2.VideoWriter('.\\picture' + "\\{}.mp4v".format(now_time), self.fourcc, 20,
                              (height, width))
        for ig in self.video:
            ig = cv2.flip(ig, 1)
            out.write(ig)
        out.release()

    # 打开摄像头，采集视频
    def open_camera(self):
        self.mopi_flag = False
        self.meibai_flag = False
        flag = self.cap.open(0, cv2.CAP_DSHOW)
        if not flag:
            QMessageBox.information(self, "警告", "该设备未正常连接", QMessageBox.Ok)
        else:
            self.video_label.setEnabled(True)  # 设置视频展示label可用
            self.actionopenvideo.setEnabled(False)  # 设置打开摄像头按钮不可用
            self.actionclosevideo.setEnabled(True)  # 设置关闭摄像头可用
            self.timer.start()  # 开启定时器

    # 关闭摄像头
    def close_camera(self):
        self.cap.release()  # 释放摄像头设备
        self.video_label.clear()  # 清空视频展示画面
        self.actionopenvideo.setEnabled(True)  # 使打开摄像头按钮可用
        self.actionclosevideo.setEnabled(False)  # 使关闭摄像头不可用
        self.timer.stop()

    # 打开本地视频文件
    def get_open(self):
        self.actionstart_T.setEnabled(True)  # 当打开文件是视频时，将开始播放按钮设置为可点击状态
        self.actionclose_L.setEnabled(True)  # 设置关闭视频按钮可用
        self.mopi_flag = False
        self.meibai_flag = False
        flag = False  # 标记图片格式是否正确
        dig = QFileDialog()
        dig.setFileMode(QFileDialog.AnyFile)
        dig.setFilter(QDir.Files)
        video_type = [".mp4", ".mkv", ".MOV", ".avi"]
        if dig.exec_():
            filename = dig.selectedFiles()
            try:
                self.current_path = filename[0]  # 获取当前视频文件的地址
                for ve in video_type:  # 判断文件格式是否正确
                    if ve not in self.current_path:
                        continue
                    else:
                        flag = True  # 打开视频格式正确
                        self.cap.open(self.current_path)  # 打开视频
                        self.timer.start(30)
                        self.playing = True
                        self.actionstart_T.setEnabled(False)  # 将开始播放按钮设置为不可点击状态
                        self.actiontimeout_E.setEnabled(True)  # 将暂停播放按钮设置为可点击状态
                if not flag:
                    QMessageBox.information(self, "警告", "暂不支持此格式文件！", QMessageBox.Ok)
            except Exception:
                QMessageBox.critical(None, '错误', '文件打开失败', QMessageBox.Ok)

    # 播放本地视频
    def play_video(self):
        self.actionstart_T.setEnabled(False)  # 当打开文件是视频时，将开始播放按钮设置为不可点击状态
        self.actiontimeout_E.setEnabled(True)  # 设置暂停播放按钮为可点击状态
        self.timer.blockSignals(False)  # 视频流阻塞信号关闭
        # 如果计时器没激活，证明是暂停状态，需要重新播放，并把self.playing设为True
        if self.timer.isActive() is False:
            self.cap.open(self.current_path)  # 打开视频
            self.timer.start(30)
            self.playing = True
            self.actionstart_T.setEnabled(False)  # 将开始播放按钮设置为不可点击状态
            self.actiontimeout_E.setEnabled(True)  # 将暂停播放按钮设置为可点击状态
        # 如果计时器激活了，并且num为奇数，证明是播放状态，需要暂停播放，并把self.playing设为False
        elif self.timer.isActive() is True and self.num % 2 == 1:
            self.timer.blockSignals(True)
            self.playing = False
            self.num += 1
            self.actionstart_T.setEnabled(True)  # 将开始播放按钮设置为可点击状态
            self.actiontimeout_E.setEnabled(False)  # 将暂停播放按钮设置为不可点击状态
        # 如果计时器激活了，并且num为偶数，证明经过播放阶段，现在是暂停状态，需要重新开始播放，并把self.playing设置为True
        elif self.timer.isActive() is True and self.num % 2 == 0:
            self.num += 1
            self.timer.blockSignals(False)
            self.playing = True
            self.actionstart_T.setEnabled(False)  # 将开始播放按钮设置为不可点击状态
            self.actiontimeout_E.setEnabled(True)  # 将暂停播放按钮设置为可点击状态
        # 否则，表示视频播放错误
        else:
            QMessageBox.information(self, "警告", "视频播放错误！", QMessageBox.Ok)

    # 关闭视频
    def close_video(self):
        self.cap.release()  # 释放摄像头设备
        self.actionstart_T.setEnabled(True)  # 设置开始播放按钮可用
        self.actiontimeout_E.setEnabled(False)  # 设置暂停播放按钮不可用
        self.actionclose_L.setEnabled(False)  # 设置关闭视频按钮不可用
        self.video_label.clear()  # 清空视频展示画面
        self.timer.stop()  # 停止定时器
        self.playing = False

    # 播放视频画面
    def init_timer(self):
        self.timer = QTimer(self)  # 创建定时器
        self.timer.timeout.connect(self.show_pic)  # 当定时器超时时展示视频图像

    # 显示视频图像
    def show_pic(self):
        ret, img = self.cap.read()
        if ret:
            img = cv2.flip(img, 1)  # 左右翻转
            if self.mopi_flag:  # 判断是否进行磨皮操作
                img = self.get_buffing(img)
            elif self.mopi_pushButton.isDown():
                self.mopi_flag = True
            if self.meibai_flag:
                img = self.get_whitening(img)
            elif self.meibai_pushButton.isDown():
                self.meibai_flag = True
            self.video.append(img)  # 将当前帧存入video中
            cur_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 将图像转为灰度图像
            # 视频流的长和宽
            height, width = cur_frame.shape[:2]
            pixmap = QImage(cur_frame, width, height, QImage.Format_RGB888)
            # 自适应窗口大小
            pixmap = QPixmap.fromImage(pixmap).scaled(self.video_label.width(), self.video_label.height())
            # 视频流置于label中间播放
            self.video_label.setAlignment(Qt.AlignCenter)
            self.video_label.setPixmap(pixmap)

    # 磨皮
    def get_buffing(self, image):
        image = np.array(image, dtype=np.uint8)
        output = Buffing_Whitening203.buffing(image, self.d, self.mopi_horizontalSlider.value(),
                                              self.mopi_horizontalSlider.value())
        return output

    # 美白
    def get_whitening(self, image):
        image = np.array(image, dtype=np.uint8)
        output = Buffing_Whitening203.whitening(image,self.meibai_horizontalSlider.value())
        return output


class myCameraWindow(QtWidgets.QMainWindow, CameraWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fps = None
        self.end_time = None
        self.start_time = None
        self.setupUi(self)
        self.beautify_window()  # 美化界面
        self.mainWindow = None
        self.current_path = None  # 初始化文件路径记录
        self.timer = None  # 初始化定时器
        self.cap = cv2.VideoCapture()  # 获取摄像头设备
        self.image = None  # 初始化照片
        self.video = None  # 初始化视频
        self.picture_or_video = False  # 标记按钮是拍照还是录像
        self.video_num = 1  # 标记是否开始或结束录像

        # 确定视频的编码格式
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        # 存储视频
        self.video_image = []

        self.relevancy()
        self.init_timer()

    # 美化界面
    def beautify_window(self):
        self.resize(900, 850)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setIconSize(QSize(40, 40))
        win_icon = qtawesome.icon('fa5b.optin-monster', color='orange')  # 设置窗口图标
        self.setWindowIcon(win_icon)
        open_icon = qtawesome.icon('ri.folder-open-line', color='white')  # 设置打开图标
        self.actionopen_O.setIcon(open_icon)
        delete_icon = qtawesome.icon('ri.delete-bin-line', color='white')  # 设置删除图标
        self.actiondelete_D.setIcon(delete_icon)
        save_icon = qtawesome.icon('ri.save-3-line', color='white')  # 设置保存图标
        self.actionsave_S.setIcon(save_icon)
        picture_icon = qtawesome.icon('ei.camera', color='white')  # 设置拍照图标
        self.actionpicture_P.setIcon(picture_icon)
        video_icon = qtawesome.icon('fa5s.video', color='white')  # 设置摄像图标
        self.actionvideo_V.setIcon(video_icon)
        get_icon = qtawesome.icon('fa.dot-circle-o', color='white')  # 设置获取图标
        self.get_pushButton.setIcon(get_icon)
        self.get_pushButton.setIconSize(QSize(80, 80))

    # 关联组件与事件
    def relevancy(self):
        self.actionopen_O.triggered.connect(self.get_open)
        self.actionsave_S.triggered.connect(self.get_Save)
        self.actiondelete_D.triggered.connect(self.get_delete)
        self.actionpicture_P.triggered.connect(self.open_camera)
        self.actionvideo_V.triggered.connect(self.open_video)
        self.get_pushButton.clicked.connect(self.camera_or_video)

    # 重写关闭按钮事件，关闭本窗口，返回主窗口
    def closeEvent(self, event):
        self.mainWindow = myMainWindow()
        self.mainWindow.show()
        self.close()

    # 打开图像文件
    def get_open(self):
        flag = False  # 标记图片格式是否正确
        self.timer.stop()  # 关闭定时器L
        self.show_label.clear()
        dig = QFileDialog()
        dig.setFileMode(QFileDialog.AnyFile)
        dig.setFilter(QDir.Files)
        img_type = [".bmp", ".jpg", ".png", ".gif"]  # 定义可打开的图像文件类型
        video_type = [".mp4", ".mkv", ".MOV", ".avi"]  # 定义可打开的视频文件类型
        if dig.exec_():
            filename = dig.selectedFiles()
            try:
                self.current_path = filename[0]  # 获取当前视频文件的地址
                for ve in video_type:  # 判断文件格式是否正确
                    if ve not in self.current_path:
                        continue
                    else:
                        flag = True  # 打开图片格式正确
                        self.cap.open(self.current_path)  # 打开视频
                        self.timer.start(30)
                if not flag:
                    for ig in img_type:
                        if ig not in self.current_path:
                            continue
                        else:
                            flag = True  # 打开图片格式正确
                            # 获取图片并自适应窗口大小
                            img = QPixmap(filename[0]).scaled(self.show_label.width(), self.show_label.height())
                            self.show_label.setPixmap(img)
                            self.show_label.setScaledContents(True)
                if not flag:
                    QMessageBox.information(self, "警告", "暂不支持此格式文件！", QMessageBox.Ok)
            except Exception:
                QMessageBox.critical(None, '错误', '文件打开失败', QMessageBox.Ok)

    # 播放视频画面
    def init_timer(self):
        self.timer = QTimer(self)  # 创建定时器
        self.timer.timeout.connect(self.show_pic)  # 当定时器超时时展示视频图像

    # 显示视频图像
    def show_pic(self):
        ret, self.image = self.cap.read()
        if ret:
            self.image = cv2.flip(self.image, 1)  # 左右翻转
            self.video_image.append(self.image)
            cur_frame = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)  # 将图像转为灰度图像
            # 视频流的长和宽
            height, width = cur_frame.shape[:2]
            pixmap = QImage(cur_frame, width, height, QImage.Format_RGB888)
            # 自适应窗口大小
            pixmap = QPixmap.fromImage(pixmap).scaled(self.show_label.width(), self.show_label.height())
            # 视频流置于label中间播放
            self.show_label.setAlignment(Qt.AlignCenter)
            self.show_label.setPixmap(pixmap)

    # 为保存菜单创建关联事件
    def get_Save(self):
        data = self.show_label.pixmap().toImage()
        fpath, ftype = QFileDialog.getSaveFileName(self, '保存图片', ".\\",
                                                   "*.jpg;;*.png;;*.bmp;;*.gif;;"
                                                   "*.mp4;;*.mkv;;*.MOV;;*.avi;;"
                                                   "All Files(*)")
        self.current_path = fpath
        data.save(fpath)

    # 为删除菜单创建关联事件
    def get_delete(self):
        select = QMessageBox.information(None, '删除', '是否确定删除该文件？', QMessageBox.Yes | QMessageBox.No)
        if select == QMessageBox.Yes:
            self.show_label.clear()
            os.remove(self.current_path)

    # 为get_pushbutton关联事件
    def camera_or_video(self):
        if not self.picture_or_video:
            self.get_picture()
        else:
            self.get_video()

    # 打开摄像头
    def open_camera(self):
        self.picture_or_video = False  # 标记此时是拍照
        flag = self.cap.open(0, cv2.CAP_DSHOW)
        if not flag:
            QMessageBox.information(self, "警告", "该设备未正常连接", QMessageBox.Ok)
        else:
            self.show_label.setEnabled(True)  # 设置视频展示label可用
            self.actionvideo_V.setEnabled(True)  # 设置摄像按钮可用
            self.actionpicture_P.setEnabled(False)  # 设置打开摄像头按钮不可用
            self.timer.start()  # 开启定时器

    # 获取照片
    def get_picture(self):
        if self.timer.isActive() is True:
            now_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))  # 获取拍摄时间
            if not os.path.exists('.\\picture'):
                os.makedirs('.\\picture')
            cv2.imencode('.jpg', self.image)[1].tofile('.\\picture\\pic_' + str(now_time) + '.jpg')

    # 打开摄像头
    def open_video(self):
        self.picture_or_video = True  # 标记此时是录像
        flag = self.cap.open(0, cv2.CAP_DSHOW)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        if not flag:
            QMessageBox.information(self, "警告", "该设备未正常连接", QMessageBox.Ok)
        else:
            self.show_label.setEnabled(True)  # 设置视频展示label可用
            self.actionpicture_P.setEnabled(True)  # 设置拍照按钮可用
            self.actionvideo_V.setEnabled(False)  # 设置打开摄像头按钮不可用

    # 开始录像
    def start_video(self):
        self.timer.start()  # 开启定时器
        self.video_num += 1

    # 结束录像
    def end_video(self):
        self.timer.stop()  # 关闭定时器
        self.video_num += 1

    # 获取录像
    def get_video(self):
        # 若video_num为奇数，表示开始录像
        if self.video_num % 2 == 1:
            self.start_video()
            self.start_time = time.perf_counter()
        # 若video_num为偶数，表示结束录像
        elif self.video_num % 2 == 0:
            self.end_video()
            self.end_time = time.perf_counter()
            now_time = fr"video{time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))}"  # 获取拍摄时间
            if not os.path.exists('.\\picture'):
                os.makedirs('.\\picture')
            self.cap.release()  # 释放摄像头
            width, height = self.image.shape[:2]
            out = cv2.VideoWriter('.\\picture' + "\\{}.mp4v".format(now_time), self.fourcc, 20,
                                  (height, width))
            for ig in self.video_image:
                ig = cv2.flip(ig, 1)
                out.write(ig)
            out.release()
        else:
            QMessageBox.information(self, "警告", "录像出现异常错误！", QMessageBox.Ok)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainPageWindow = myMainWindow()
    MainPageWindow.show()
    sys.exit(app.exec_())
