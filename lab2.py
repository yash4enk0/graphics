import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import QTimer
from OpenGL.GL import *
import math

class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0.0
        self.shape_type = 'cube'
        self.render_mode = 'fill'
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateRotation)
        self.timer.start(20)
    
    def initializeGL(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)
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
        
        if self.render_mode == 'point':
            glPolygonMode(GL_FRONT_AND_BACK, GL_POINT)
            glPointSize(8.0)
            glEnable(GL_POINT_SMOOTH)
        elif self.render_mode == 'line':
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glLineWidth(2.0)
            glEnable(GL_LINE_SMOOTH)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        if self.shape_type == 'cube':
            self.drawCube()
        elif self.shape_type == 'prism':
            self.drawPrism()
        elif self.shape_type == 'pyramid':
            self.drawPyramid()
        
        glPopMatrix()
    
    def drawCube(self):
        h = 1.0
        
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_QUADS)
        glNormal3f(0.0, 0.0, 1.0)
        glVertex3f(h, h, h)
        glVertex3f(-h, h, h)
        glVertex3f(-h, -h, h)
        glVertex3f(h, -h, h)
        glEnd()
        
        glColor3f(0.0, 0.0, 1.0)
        glBegin(GL_QUADS)
        glNormal3f(1.0, 0.0, 0.0)
        glVertex3f(h, h, -h)
        glVertex3f(h, h, h)
        glVertex3f(h, -h, h)
        glVertex3f(h, -h, -h)
        glEnd()
        
        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_QUADS)
        glNormal3f(0.0, 0.0, -1.0)
        glVertex3f(-h, h, -h)
        glVertex3f(h, h, -h)
        glVertex3f(h, -h, -h)
        glVertex3f(-h, -h, -h)
        glEnd()
        
        glColor3f(1.0, 1.0, 0.0)
        glBegin(GL_QUADS)
        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(-h, h, h)
        glVertex3f(-h, h, -h)
        glVertex3f(-h, -h, -h)
        glVertex3f(-h, -h, h)
        glEnd()
        
        glColor3f(1.0, 0.0, 1.0)
        glBegin(GL_QUADS)
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(h, h, h)
        glVertex3f(h, h, -h)
        glVertex3f(-h, h, -h)
        glVertex3f(-h, h, h)
        glEnd()
        
        glColor3f(0.0, 1.0, 1.0)
        glBegin(GL_QUADS)
        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(h, -h, h)
        glVertex3f(-h, -h, h)
        glVertex3f(-h, -h, -h)
        glVertex3f(h, -h, -h)
        glEnd()
    
    def drawPrism(self):
        n = 16
        h = 1.0
        r = 0.5
        delta_fi = 2 * math.pi / n
        
        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_QUADS)
        for i in range(n):
            fi = i * delta_fi
            nx = math.cos(fi + delta_fi / 2)
            ny = math.sin(fi + delta_fi / 2)
            glNormal3f(nx, ny, 0.0)
            
            glVertex3f(r * math.cos(fi), r * math.sin(fi), h / 2)
            glVertex3f(r * math.cos(fi), r * math.sin(fi), -h / 2)
            glVertex3f(r * math.cos(fi + delta_fi), r * math.sin(fi + delta_fi), -h / 2)
            glVertex3f(r * math.cos(fi + delta_fi), r * math.sin(fi + delta_fi), h / 2)
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
    
    def drawPyramid(self):
        n = 16
        h = 1.0
        r = 0.5
        delta_fi = 2 * math.pi / n
        teta = math.atan(h / r)
        
        glBegin(GL_TRIANGLES)
        for i in range(n):
            fi = i * delta_fi
            glColor3f((i % 2), ((i % 3) / 2), ((i % 5) / 4))
            
            nx = math.cos(fi + delta_fi / 2) * math.sin(teta)
            ny = math.sin(fi + delta_fi / 2) * math.sin(teta)
            nz = math.cos(teta)
            glNormal3f(nx, ny, nz)
            
            glVertex3f(0, 0, h)
            glVertex3f(r * math.cos(fi), r * math.sin(fi), 0)
            glVertex3f(r * math.cos(fi + delta_fi), r * math.sin(fi + delta_fi), 0)
        glEnd()
        
        glBegin(GL_POLYGON)
        glColor3f(0.8, 0.8, 0.0)
        glNormal3f(0, 0, -1)
        for i in range(n - 1, -1, -1):
            fi = i * delta_fi
            glVertex3f(r * math.cos(fi), r * math.sin(fi), 0)
        glEnd()
    
    def setShape(self, shape):
        self.shape_type = shape
        self.update()
    
    def setRenderMode(self, mode):
        self.render_mode = mode
        self.update()
    
    def updateRotation(self):
            self.angle += 1.0
            if self.angle >= 360.0:
                self.angle = 0.0
            self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lab №2 - Yashchenko Oleksandra, IC-34")
        self.setFixedSize(900, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        self.opengl_widget = OpenGLWidget()
        layout.addWidget(self.opengl_widget)
        
        shape_layout = QHBoxLayout()
        
        cube_btn = QPushButton("Куб")
        cube_btn.clicked.connect(lambda: self.opengl_widget.setShape('cube'))
        shape_layout.addWidget(cube_btn)
        
        prism_btn = QPushButton("Призма")
        prism_btn.clicked.connect(lambda: self.opengl_widget.setShape('prism'))
        shape_layout.addWidget(prism_btn)
        
        pyramid_btn = QPushButton("Піраміда")
        pyramid_btn.clicked.connect(lambda: self.opengl_widget.setShape('pyramid'))
        shape_layout.addWidget(pyramid_btn)
        
        layout.addLayout(shape_layout)
        
        render_layout = QHBoxLayout()
        
        fill_btn = QPushButton("Суцільна")
        fill_btn.clicked.connect(lambda: self.opengl_widget.setRenderMode('fill'))
        render_layout.addWidget(fill_btn)
        
        line_btn = QPushButton("Каркас")
        line_btn.clicked.connect(lambda: self.opengl_widget.setRenderMode('line'))
        render_layout.addWidget(line_btn)
        
        point_btn = QPushButton("Точки")
        point_btn.clicked.connect(lambda: self.opengl_widget.setRenderMode('point'))
        render_layout.addWidget(point_btn)
        
        layout.addLayout(render_layout)
        
        central_widget.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()