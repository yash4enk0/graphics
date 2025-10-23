import sys
import numpy as np
import math
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt
from OpenGL.GL import *
from PIL import Image

class GLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.angle_x = 20.0
        self.angle_y = 30.0
        self.last_pos = None
        self.TW = 512
        self.TH = 512
        self.arrayRGB = np.zeros((self.TH, self.TW, 3), dtype=np.uint8)
        self.mult = 1.0
        self.texture_ready = False
        self.texture_id = None
        
    def initializeGL(self):
        glClearColor(0.2, 0.2, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.set_perspective()
        glMatrixMode(GL_MODELVIEW)
        
        self.calculate_checkerboard_texture()
        self.setup_texture()
        self.texture_ready = True
        
    def set_perspective(self):
        w = self.width()
        h = self.height()
        
        if h == 0:
            h = 1
        aspect = w / h
        fov = 45.0 * math.pi / 180.0
        f = 1.0 / math.tan(fov / 2.0)
        znear = 0.1
        zfar = 50.0
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        matrix = [
            f / aspect, 0, 0, 0,
            0, f, 0, 0,
            0, 0, (zfar + znear) / (znear - zfar), -1,
            0, 0, (2 * zfar * znear) / (znear - zfar), 0
        ]
        glMultMatrixf(matrix)
        glMatrixMode(GL_MODELVIEW)
        
    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        self.set_perspective()
        
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        glTranslatef(0, 0, -5)
        glRotatef(self.angle_x, 1, 0, 0)
        glRotatef(self.angle_y, 0, 1, 0)
        
        if self.texture_ready:
            self.draw_textured_cube()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_pos = event.pos()
        
    def mouseMoveEvent(self, event):
        if self.last_pos:
            dx = event.pos().x() - self.last_pos.x()
            dy = event.pos().y() - self.last_pos.y()
            self.angle_y += dx * 0.5
            self.angle_x += dy * 0.5
            self.last_pos = event.pos()
            self.update()
            
    def mouseReleaseEvent(self, event):
        self.last_pos = None
        
    def load_bmp_texture(self, filename):
        try:
            img = Image.open(filename)
            img = img.resize((self.TW, self.TH))
            img = img.convert('RGB')
            
            img_data = np.array(img, dtype=np.uint8)
            self.arrayRGB = np.flipud(img_data)
            
            return True
        except Exception as e:
            print(f"Error loading texture: {e}")
            return False
            
    def calculate_checkerboard_texture(self):
        light_color = np.array([210, 180, 140], dtype=np.uint8)
        dark_color = np.array([101, 67, 33], dtype=np.uint8)
        
        for i in range(self.TW):
            for j in range(self.TH):
                if (i < self.TW // 2 and j < self.TH // 2) or (i >= self.TW // 2 and j >= self.TH // 2):
                    self.arrayRGB[j, i] = dark_color
                else:
                    self.arrayRGB[j, i] = light_color
        
    def calculate_pattern_texture(self):
        for i in range(self.TW):
            for j in range(self.TH):
                x = (i - self.TW // 2) / self.TW * 8
                y = (j - self.TH // 2) / self.TH * 8
                r = math.sqrt(x * x + y * y)
                fi = math.atan(y / x) if x != 0.0 else math.pi / 2
                value = abs(math.cos(8 * fi - r))
                
                if (value % 1.0) < 0.75:
                    self.arrayRGB[j, i] = [255, 255, 0]
                else:
                    self.arrayRGB[j, i] = [0, 0, 255]
        
    def setup_texture(self):
        glEnable(GL_TEXTURE_2D)
        
        if self.texture_id is not None:
            glDeleteTextures([self.texture_id])
        
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.TW, self.TH, 0, GL_RGB, GL_UNSIGNED_BYTE, self.arrayRGB)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glDisable(GL_TEXTURE_2D)
        
    def draw_textured_cube(self):
        h = 1.0
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        glMatrixMode(GL_TEXTURE)
        glLoadIdentity()
        glScalef(self.mult, self.mult, self.mult)
        glMatrixMode(GL_MODELVIEW)
        
        glBegin(GL_QUADS)
        
        glTexCoord2f(1, 1); glVertex3f( h,  h,  h)
        glTexCoord2f(0, 1); glVertex3f(-h,  h,  h)
        glTexCoord2f(0, 0); glVertex3f(-h, -h,  h)
        glTexCoord2f(1, 0); glVertex3f( h, -h,  h)
        
        glTexCoord2f(1, 1); glVertex3f( h,  h, -h)
        glTexCoord2f(0, 1); glVertex3f( h,  h,  h)
        glTexCoord2f(0, 0); glVertex3f( h, -h,  h)
        glTexCoord2f(1, 0); glVertex3f( h, -h, -h)
        
        glTexCoord2f(1, 1); glVertex3f(-h,  h, -h)
        glTexCoord2f(0, 1); glVertex3f( h,  h, -h)
        glTexCoord2f(0, 0); glVertex3f( h, -h, -h)
        glTexCoord2f(1, 0); glVertex3f(-h, -h, -h)
        
        glTexCoord2f(1, 1); glVertex3f(-h,  h,  h)
        glTexCoord2f(0, 1); glVertex3f(-h,  h, -h)
        glTexCoord2f(0, 0); glVertex3f(-h, -h, -h)
        glTexCoord2f(1, 0); glVertex3f(-h, -h,  h)
        
        glTexCoord2f(1, 1); glVertex3f(-h,  h,  h)
        glTexCoord2f(0, 1); glVertex3f( h,  h,  h)
        glTexCoord2f(0, 0); glVertex3f( h,  h, -h)
        glTexCoord2f(1, 0); glVertex3f(-h,  h, -h)
        
        glTexCoord2f(1, 1); glVertex3f( h, -h,  h)
        glTexCoord2f(0, 1); glVertex3f(-h, -h,  h)
        glTexCoord2f(0, 0); glVertex3f(-h, -h, -h)
        glTexCoord2f(1, 0); glVertex3f( h, -h, -h)
        
        glEnd()
        
        glDisable(GL_TEXTURE_2D)
        
        glMatrixMode(GL_TEXTURE)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        
    def change_scale(self, delta):
        self.mult += delta
        self.mult = max(0.25, self.mult)
        self.update()
        
    def reset_scale(self):
        self.mult = 1.0
        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lab 4: 2D Textures - Yashchenko IS-34")
        self.setGeometry(100, 100, 900, 700)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        self.gl_widget = GLWidget()
        layout.addWidget(self.gl_widget)
        
        controls_layout = QHBoxLayout()
        
        info_label = QLabel("Завдання 3: 2D Текстури")
        info_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        controls_layout.addWidget(info_label)
        
        controls_layout.addStretch()
        
        btn1 = QPushButton("Завдання 3.2: Текстура з файлу")
        btn1.clicked.connect(self.load_texture)
        controls_layout.addWidget(btn1)
        
        btn2 = QPushButton("Завдання 3.3: Шахівниця")
        btn2.clicked.connect(self.load_checkerboard)
        controls_layout.addWidget(btn2)
        
        btn3 = QPushButton("Завдання 3.4: Візерунок")
        btn3.clicked.connect(self.load_pattern)
        controls_layout.addWidget(btn3)
        
        controls_layout.addStretch()
        
        btn_minus = QPushButton("Масштаб -")
        btn_minus.clicked.connect(lambda: self.gl_widget.change_scale(-0.25))
        controls_layout.addWidget(btn_minus)
        
        btn_plus = QPushButton("Масштаб +")
        btn_plus.clicked.connect(lambda: self.gl_widget.change_scale(0.25))
        controls_layout.addWidget(btn_plus)
        
        btn_reset = QPushButton("Скинути")
        btn_reset.clicked.connect(self.gl_widget.reset_scale)
        controls_layout.addWidget(btn_reset)
        
        layout.addLayout(controls_layout)
        
    def load_texture(self):
        if self.gl_widget.load_bmp_texture('media/texture.bmp'):
            self.gl_widget.setup_texture()
            self.gl_widget.update()
        
    def load_checkerboard(self):
        self.gl_widget.calculate_checkerboard_texture()
        self.gl_widget.setup_texture()
        self.gl_widget.update()
        
    def load_pattern(self):
        self.gl_widget.calculate_pattern_texture()
        self.gl_widget.setup_texture()
        self.gl_widget.update()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()