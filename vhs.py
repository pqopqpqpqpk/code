import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QSlider
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPixmap, QImage
import cv2
import numpy as np

class KeyframeEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("키프레임 영상 편집기")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("영상 없음")
        self.layout.addWidget(self.label)

        self.load_btn = QPushButton("영상 불러오기")
        self.load_btn.clicked.connect(self.load_video)
        self.layout.addWidget(self.load_btn)

        self.add_kf_btn = QPushButton("키프레임 추가")
        self.add_kf_btn.clicked.connect(self.add_keyframe)
        self.layout.addWidget(self.add_kf_btn)

        self.slider = QSlider()
        self.slider.setOrientation(1)  # Horizontal
        self.layout.addWidget(self.slider)

        self.play_btn = QPushButton("재생")
        self.play_btn.clicked.connect(self.play_video)
        self.layout.addWidget(self.play_btn)

        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)
        self.frame_pos = 0
        self.frames = []
        self.keyframes = {}  # frame_number : {'x':0, 'y':0}

    def load_video(self):
        fname, _ = QFileDialog.getOpenFileName(self, "영상 선택", "", "Video Files (*.mp4 *.avi)")
        if fname:
            self.cap = cv2.VideoCapture(fname)
            self.frames = []
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                self.frames.append(frame)
            self.slider.setMaximum(len(self.frames)-1)
            self.label.setText("영상 불러옴")

    def add_keyframe(self):
        # 현재 슬라이더 위치의 키프레임 추가 (예: x, y 이동)
        frame_num = self.slider.value()
        x = 0
        y = 0
        # 예시: y 위치를 2픽셀 떨림 효과
        y = 2 if frame_num % 2 == 0 else -2
        self.keyframes[frame_num] = {'x': x, 'y': y}
        self.label.setText(f"키프레임 추가: {frame_num}")

    def play_video(self):
        self.frame_pos = 0
        self.timer.start(30)  # FPS 조절 가능

    def next_frame(self):
        if self.frame_pos >= len(self.frames):
            self.timer.stop()
            return

        frame = self.frames[self.frame_pos].copy()

        # 키프레임 적용 (보간 없이 단순 적용)
        if self.frame_pos in self.keyframes:
            kf = self.keyframes[self.frame_pos]
            M = np.float32([[1, 0, kf['x']], [0, 1, kf['y']]])
            frame = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))

        # OpenCV -> QImage 변환
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.label.setPixmap(pixmap.scaled(self.label.width(), self.label.height()))

        self.frame_pos += 1
        self.slider.setValue(self.frame_pos)

app = QApplication(sys.argv)
editor = KeyframeEditor()
editor.show()
sys.exit(app.exec())
