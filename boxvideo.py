import sys
import cv2
import argparse
import multiprocessing
import os
import pygame
from pygame import mixer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtGui import QImage, QPixmap
from pydub import AudioSegment

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self, video_path, size):
        super().__init__()
        self._run_flag = True
        self.video_path = video_path
        self.size = size
        self.video_duration = None

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            print(f"Error: Unable to open video file {self.video_path}")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        delay = int(1000 / fps) if fps > 0 else 33  # Default to ~30 fps if fps is 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.video_duration = total_frames / fps  # in seconds

        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)  # Initialize pygame mixer

        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                p = convert_to_Qt_format.scaled(self.size[0], self.size[1], Qt.KeepAspectRatio)
                self.change_pixmap_signal.emit(p)
                QThread.msleep(delay)

                pygame.mixer.music.unpause()  # Unpause music to sync with video frames
            else:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                pygame.mixer.music.pause()  # Pause music when video restarts
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()

class VideoWindow(QMainWindow):
    def __init__(self, video_path, size=(120, 120), sound=False):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(size[0], size[1])

        self.label = QLabel(self)
        self.label.setFixedSize(size[0], size[1])
        self.label.setAlignment(Qt.AlignCenter)  # Center align the label
        layout = QVBoxLayout()
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.thread = VideoThread(video_path, size)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

        self.offset = None

        if sound:
            audio_path = os.path.expanduser("~/.local/share/boxvideo/sound.mp3")
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)
            if os.path.exists(audio_path):
                os.remove(audio_path)
            audio_process = multiprocessing.Process(target=self.extract_and_play_audio, args=(video_path, audio_path))
            audio_process.start()
            self.audio_process = audio_process

    def extract_and_play_audio(self, video_path, audio_path):
        audio = AudioSegment.from_file(video_path)
        audio.export(audio_path, format="mp3")

        mixer.init()  # Initialize pygame mixer
        mixer.music.load(audio_path)
        mixer.music.play()

        while True:
            pygame.time.Clock().tick(10)  # Adjust tick rate as needed
            if not mixer.music.get_busy():
                mixer.music.play()

    @pyqtSlot(QImage)
    def update_image(self, qimage):
        self.label.setPixmap(QPixmap.fromImage(qimage))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.offset is not None:
            x = event.globalX() - self.offset.x()
            y = event.globalY() - self.offset.y()
            self.move(x, y)

    def mouseReleaseEvent(self, event):
        self.offset = None

    def closeEvent(self, event):
        self.thread.stop()
        if hasattr(self, 'audio_process'):
            self.audio_process.terminate()
        event.accept()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play a video in a small, draggable, always-on-top window.")
    parser.add_argument("video_path", help="Path to the video file.")
    parser.add_argument("size", nargs="?", default="120x120", help="Size of the video window in WIDTHxHEIGHT format.")
    parser.add_argument("--sound", action="store_true", help="Play video with sound.")

    args = parser.parse_args()

    try:
        width, height = map(int, args.size.split('x'))
    except ValueError:
        print("Error: Size must be in WIDTHxHEIGHT format.")
        sys.exit(1)

    app = QApplication(sys.argv)
    window = VideoWindow(args.video_path, size=(width, height), sound=args.sound)
    window.show()
    sys.exit(app.exec_())
