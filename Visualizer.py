from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QSlider, QLineEdit
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont
from PyQt5.QtCore import Qt, QBasicTimer
from Body import *
import sys
import numpy as np


SUN_MASS = 1.989e30
SUN_RADIUS = 696340000


def create_label(name, number, window):
    label = QLabel(window)
    label.setText(name)
    label.resize(Animation.ADDS, Animation.SIZE // (2 * Animation.NO_OPTIONS))
    label.move(0, number * Animation.SIZE // Animation.NO_OPTIONS)
    label.setFont(QFont("Times", Animation.SIZE // 30))
    return label


def create_button(name, number, window, func):
    button = QPushButton(name, window)
    button.move(0, number * Animation.SIZE // Animation.NO_OPTIONS + Animation.SIZE // (2 * Animation.NO_OPTIONS))
    button.setFont(QFont("Times", Animation.SIZE // 40))
    button.resize(Animation.ADDS, Animation.SIZE // (2 * Animation.NO_OPTIONS))
    button.clicked.connect(func)
    return button


class Animation(QMainWindow):
    dt = 100
    SIZE = 900
    ADDS = SIZE // 2
    NO_OPTIONS = 5

    def __init__(self, sth):
        super().__init__()
        self.setWindowTitle("Projekt")
        self.setGeometry(300, 100, Animation.SIZE + Animation.ADDS, Animation.SIZE)
        self.space = sth

        self.ZOOM = 1000
        for body in self.space:
            self.ZOOM = max(body.x, body.y, self.ZOOM)
        self.ZOOM *= 1.5

        self.state = 0
        self.start_x = 0
        self.start_y = 0
        self.delta_x = 0
        self.delta_y = 0
        self.inner = False

        create_label("Stop animation", 0, self)
        create_label("Add body (mass of Suns)", 1, self)
        create_label("Remove body", 2, self)
        create_label("Speed of animation", 3, self)
        create_label("Cancel action", 4, self)

        create_button("STOP", 0, self, self.stop)
        self.addButton = create_button("ADD", 1, self, self.add)
        self.addButton.resize(Animation.ADDS // 2, Animation.SIZE // (2 * Animation.NO_OPTIONS))
        self.removeButton = create_button("REMOVE", 2, self, self.remove)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.move(Animation.ADDS // 2, Animation.SIZE // Animation.NO_OPTIONS + Animation.SIZE // (2 * Animation.NO_OPTIONS))
        self.lineEdit.resize(Animation.ADDS // 2, Animation.SIZE // (2 * Animation.NO_OPTIONS))
        self.lineEdit.setFont(QFont("Times", Animation.SIZE // 40))
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.move(0, 3 * Animation.SIZE // Animation.NO_OPTIONS + Animation.SIZE // (2 * Animation.NO_OPTIONS))
        self.slider.resize(Animation.ADDS, Animation.SIZE // (2 * Animation.NO_OPTIONS))
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        create_button("CANCEL", 4, self, self.cancel)

        self.timer = QBasicTimer()
        self.timer.start(5, self)

    def stop(self):
        self.slider.setValue(0)

    def add(self):
        self.slider.setValue(0)
        self.inner = False
        self.addButton.setStyleSheet("background-color: green")
        self.removeButton.setStyleSheet(None)
        self.state = 1

    def remove(self):
        self.slider.setValue(0)
        self.inner = False
        self.addButton.setStyleSheet(None)
        self.removeButton.setStyleSheet("background-color: green")
        self.state = 2

    def cancel(self):
        self.inner = False
        self.addButton.setStyleSheet(None)
        self.removeButton.setStyleSheet(None)
        self.state = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 0, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        painter.drawRect(Animation.ADDS, 0, Animation.SIZE, Animation.SIZE)
        for body in self.space:
            painter.setPen(QPen(body.color, 0, Qt.SolidLine))
            painter.setBrush(QBrush(body.color, Qt.SolidPattern))
            body_x = int(Animation.ADDS + Animation.SIZE / 2 + (body.x+self.delta_x) / self.ZOOM * Animation.SIZE / 2 - body.size / 2)
            body_y = int(Animation.SIZE / 2 - (body.y-self.delta_y) / self.ZOOM * Animation.SIZE / 2 - body.size / 2)
            if body_x > Animation.ADDS:
                painter.drawEllipse(body_x, body_y, body.size, body.size)

    def timerEvent(self, event):
        for _ in range(5):
            merge_space(self.space)
            for body in self.space:
                F = body.calculate_force(self.space)
                body.update_speed(F, Animation.dt * self.slider.value()**2)
                body.update_position(Animation.dt * self.slider.value()**2)
        self.update()
        super(Animation, self).timerEvent(event)

    def mousePressEvent(self, event):
        if event.x() > Animation.ADDS:
            if self.state == 0:
                self.inner = True
                self.start_x = event.x()
                self.start_y = event.y()
            elif self.state == 1:
                try:
                    scale = float(self.lineEdit.text())
                except ValueError:
                    scale = 1
                x = (event.x() - Animation.ADDS - Animation.SIZE/2) * self.ZOOM / (Animation.SIZE/2) - self.delta_x
                y = - (event.y() - Animation.SIZE/2) * self.ZOOM / (Animation.SIZE/2) + self.delta_y
                self.space.append(Body(mass=scale*SUN_MASS, radius=SUN_RADIUS, size=15, x=x, y=y))
                self.state = 0
            elif self.state == 2:
                x = (event.x() - Animation.ADDS - Animation.SIZE / 2) * self.ZOOM / (Animation.SIZE / 2) - self.delta_x
                y = - (event.y() - Animation.SIZE / 2) * self.ZOOM / (Animation.SIZE / 2) + self.delta_y
                abstract_object = Body(x=x, y=y)
                new_space = []
                for body in self.space:
                    if np.linalg.norm(body.r_vector(abstract_object)) > self.ZOOM / (Animation.SIZE / 2) * body.size / 2:
                        new_space.append(body)
                self.space = new_space
                self.state = 0
            self.addButton.setStyleSheet(None)
            self.removeButton.setStyleSheet(None)
        else:
            self.inner = False

    def mouseMoveEvent(self, event):
        if self.inner:
            self.delta_x += (event.x() - self.start_x) * self.ZOOM / (Animation.SIZE / 2)
            self.delta_y += (event.y() - self.start_y) * self.ZOOM / (Animation.SIZE / 2)
            self.start_x = event.x()
            self.start_y = event.y()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.ZOOM /= 1.2
        elif event.angleDelta().y() < 0:
            self.ZOOM *= 1.2


def init_animation(idk):
    app = QApplication(sys.argv)
    anim = Animation(idk)
    anim.show()
    sys.exit(app.exec())
