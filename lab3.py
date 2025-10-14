import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import QTimer
from OpenGL.GL import *
import math

class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0.0
        self.task = 1
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateRotation)
        self.timer.start(20)
    
    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.1, 0.0, 0.2, 0.0)
        
    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        aspect = w / h if h != 0 else 1
        w_scale = 1.5 * aspect
        glOrtho(-w_scale, w_scale, -1.5, 1.5, 1, 10)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        
        glTranslatef(0.0, 0.0, -8.0)
        glRotatef(self.angle, 1.0, 1.0, 1.0)
        
        if self.task == 1:
            self.coloredCube()
        elif self.task == 2:
            self.gradientCube()
        elif self.task == 3:
            self.dynamicCube()
        elif self.task == 4:
            self.cylinder()
        elif self.task == 5:
            self.effects()
        
        glPopMatrix()

    def coloredCube(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        
        h = 1.0

        glColor3f(0.8, 0.4, 0.8)
        glBegin(GL_QUADS)
        glNormal3f(0.0, 0.0, 1.0)
        glVertex3f(h, h, h)
        glVertex3f(-h, h, h)
        glVertex3f(-h, -h, h)
        glVertex3f(h, -h, h)
        glEnd()

        glColor3f(1.0, 1.0, 0.6)
        glBegin(GL_QUADS)
        glNormal3f(1.0, 0.0, 0.0)
        glVertex3f(h, h, -h)
        glVertex3f(h, h, h)
        glVertex3f(h, -h, h)
        glVertex3f(h, -h, -h)
        glEnd()

        glColor3f(0.6, 0.3, 0.1)
        glBegin(GL_QUADS)
        glNormal3f(0.0, 0.0, -1.0)
        glVertex3f(-h, h, -h)
        glVertex3f(h, h, -h)
        glVertex3f(h, -h, -h)
        glVertex3f(-h, -h, -h)
        glEnd()

        glColor3f(0.0, 0.5, 0.5)
        glBegin(GL_QUADS)
        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(-h, h, h)
        glVertex3f(-h, h, -h)
        glVertex3f(-h, -h, -h)
        glVertex3f(-h, -h, h)
        glEnd()

        glColor3f(0.6, 0.0, 0.2)
        glBegin(GL_QUADS)
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(h, h, h)
        glVertex3f(h, h, -h)
        glVertex3f(-h, h, -h)
        glVertex3f(-h, h, h)
        glEnd()

        glColor3f(0.6, 1.0, 0.4)
        glBegin(GL_QUADS)
        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(h, -h, h)
        glVertex3f(-h, -h, h)
        glVertex3f(-h, -h, -h)
        glVertex3f(h, -h, -h)
        glEnd()

    def gradientCube(self):
        glDisable(GL_LIGHTING)
        
        h = 1.0
        
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(h, h, h)
        glVertex3f(-h, h, h)
        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(-h, -h, h)
        glVertex3f(h, -h, h)
        glEnd()

        glBegin(GL_QUADS)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(h, h, -h)
        glVertex3f(h, h, h)
        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(h, -h, h)
        glVertex3f(h, -h, -h)
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(-h, h, -h)
        glVertex3f(h, h, -h)
        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(h, -h, -h)
        glVertex3f(-h, -h, -h)
        glEnd()

        glBegin(GL_QUADS)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(-h, h, h)
        glVertex3f(-h, h, -h)
        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(-h, -h, -h)
        glVertex3f(-h, -h, h)
        glEnd()
        
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_QUADS)
        glVertex3f(h, h, h)
        glVertex3f(h, h, -h)
        glVertex3f(-h, h, -h)
        glVertex3f(-h, h, h)
        glEnd()
        
        glColor3f(1.0, 1.0, 0.0)
        glBegin(GL_QUADS)
        glVertex3f(h, -h, h)
        glVertex3f(-h, -h, h)
        glVertex3f(-h, -h, -h)
        glVertex3f(h, -h, -h)
        glEnd()

    def dynamicCube(self):
        glDisable(GL_LIGHTING)
        
        h = 1.0
        
        red_top = abs(math.sin(2 * self.angle * math.pi / 180))
        green_top = abs(math.sin(3 * self.angle * math.pi / 180))
        blue_top = abs(math.sin(5 * self.angle * math.pi / 180))
        
        red_bottom = abs(math.sin(7 * self.angle * math.pi / 180))
        green_bottom = abs(math.sin(11 * self.angle * math.pi / 180))
        blue_bottom = abs(math.sin(13 * self.angle * math.pi / 180))
        
        glBegin(GL_QUADS)
        glColor3f(red_top, green_top, blue_top)
        glVertex3f(h, h, h)
        glVertex3f(-h, h, h)
        glColor3f(red_bottom, green_bottom, blue_bottom)
        glVertex3f(-h, -h, h)
        glVertex3f(h, -h, h)
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(red_top, green_top, blue_top)
        glVertex3f(h, h, -h)
        glVertex3f(h, h, h)
        glColor3f(red_bottom, green_bottom, blue_bottom)
        glVertex3f(h, -h, h)
        glVertex3f(h, -h, -h)
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(red_top, green_top, blue_top)
        glVertex3f(-h, h, -h)
        glVertex3f(h, h, -h)
        glColor3f(red_bottom, green_bottom, blue_bottom)
        glVertex3f(h, -h, -h)
        glVertex3f(-h, -h, -h)
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(red_top, green_top, blue_top)
        glVertex3f(-h, h, h)
        glVertex3f(-h, h, -h)
        glColor3f(red_bottom, green_bottom, blue_bottom)
        glVertex3f(-h, -h, -h)
        glVertex3f(-h, -h, h)
        glEnd()
        
        glColor3f(red_top, green_top, blue_top)
        glBegin(GL_QUADS)
        glVertex3f(h, h, h)
        glVertex3f(h, h, -h)
        glVertex3f(-h, h, -h)
        glVertex3f(-h, h, h)
        glEnd()
        
        glColor3f(red_bottom, green_bottom, blue_bottom)
        glBegin(GL_QUADS)
        glVertex3f(h, -h, h)
        glVertex3f(-h, -h, h)
        glVertex3f(-h, -h, -h)
        glVertex3f(h, -h, -h)
        glEnd()
    
    def cylinder(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        
        n = 40
        h = 1.0
        r = 0.5
        delta_fi = 2 * math.pi / n
        
        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_QUAD_STRIP)
        for i in range(n + 1):
            fi = i * delta_fi
            glNormal3f(math.cos(fi), math.sin(fi), 0.0)
            glVertex3f(r * math.cos(fi), r * math.sin(fi), h / 2)
            glVertex3f(r * math.cos(fi), r * math.sin(fi), -h / 2)
        glEnd()
        
        glBegin(GL_POLYGON)
        glColor3f(1.0, 1.0, 0.0)
        glNormal3f(0, 0, 1)
        for i in range(n):
            fi = i * delta_fi
            glVertex3f(r * math.cos(fi), r * math.sin(fi), h / 2)
        glEnd()
        
        glBegin(GL_POLYGON)
        glColor3f(1.0, 0.5, 0.0)
        glNormal3f(0, 0, -1)
        for i in range(n - 1, -1, -1):
            fi = i * delta_fi
            glVertex3f(r * math.cos(fi), r * math.sin(fi), -h / 2)
        glEnd()
    
    def effects(self):
        glDisable(GL_LIGHTING)
        
        n = 80
        h = 2.0
        r = 1.0
        delta_fi = 2 * math.pi / n
        
        glBegin(GL_QUAD_STRIP)
        for i in range(n + 1):
            fi = i * delta_fi
            
            red = abs(math.sin(2 * self.angle * math.pi / 180 - fi))
            blue = abs(math.sin(3 * self.angle * math.pi / 180 - fi))
            glColor3f(red, 0.0, blue)
            glVertex3f(r * math.cos(fi), r * math.sin(fi), -h / 2)
            
            red = abs(math.sin(5 * self.angle * math.pi / 180 + fi))
            blue = abs(math.sin(7 * self.angle * math.pi / 180 + fi))
            glColor3f(red, 1.0, blue)
            glVertex3f(r * math.cos(fi), r * math.sin(fi), h / 2)
        glEnd()
    
    def setTask(self, task):
        self.task = task
        self.update()
    
    def updateRotation(self):
        self.angle += 1.0
        if self.angle >= 360.0:
            self.angle = 0.0
        self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lab №3 - Yashchenko Oleksandra, IC-34")
        self.setFixedSize(900, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        self.opengl_widget = OpenGLWidget()
        layout.addWidget(self.opengl_widget)
        
        task_layout = QHBoxLayout()
        
        task1_btn = QPushButton("2.1 Різнокольоровий куб")
        task1_btn.clicked.connect(lambda: self.opengl_widget.setTask(1))
        task_layout.addWidget(task1_btn)
        
        task2_btn = QPushButton("2.2 Градієнт")
        task2_btn.clicked.connect(lambda: self.opengl_widget.setTask(2))
        task_layout.addWidget(task2_btn)
        
        task3_btn = QPushButton("2.3 Динаміка")
        task3_btn.clicked.connect(lambda: self.opengl_widget.setTask(3))
        task_layout.addWidget(task3_btn)
        
        task4_btn = QPushButton("2.4 Циліндр")
        task4_btn.clicked.connect(lambda: self.opengl_widget.setTask(4))
        task_layout.addWidget(task4_btn)
        
        task5_btn = QPushButton("2.5 Ефекти")
        task5_btn.clicked.connect(lambda: self.opengl_widget.setTask(5))
        task_layout.addWidget(task5_btn)
        
        layout.addLayout(task_layout)
        
        central_widget.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()