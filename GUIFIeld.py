import math
import random

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush
from PySide6.QtCore import Qt, QTimer

SCALE_MULTIPLIER = 3

SPEED_SCALE_MULTIPLIER = 10


class GUIField(QWidget):

    simulation = None

    def __init__(self, simulation, height, width, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.pressed = self.moving = False
        self.init_ui(height, width)
        self.simulation = simulation
        self.init_timer()

    def init_ui(self, height, width):
        self.setFixedSize(height, width)
        self.show()

    def init_timer(self):
        timer = QTimer(self)
        timer.setInterval(50)
        timer.timeout.connect(self.update)
        timer.start(50)

    def show_walls(self, qp):
        for wall in self.simulation.field.walls:
            self.draw_wall(qp, wall.x_1 * SCALE_MULTIPLIER, wall.y_1 * SCALE_MULTIPLIER, wall.x_2 * SCALE_MULTIPLIER, wall.y_2 * SCALE_MULTIPLIER)

    def show_persons(self, qp):
        for person in self.simulation.field.persons:
            vector_angle = math.atan2(person.speed_x, person.speed_y)
            vector_len = math.sqrt(person.speed_x ** 2 + person.speed_y ** 2)
            self.draw_person(qp, person.pos_x * SCALE_MULTIPLIER, person.pos_y * SCALE_MULTIPLIER, vector_angle, vector_len)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_net(qp)
        self.draw_borders(qp)
        self.mark_borders(qp)
        self.show_walls(qp)
        self.show_persons(qp)
        qp.end()

    def draw_borders(self, qp):
        size = self.size()
        width = size.width() - 1
        height = size.height() - 1
        qp.setPen(QPen(Qt.black, 1))
        qp.drawRect(0, 0, width, height)

    def mark_borders(self, qp):
        size = self.size()
        width = size.width() - 1
        height = size.height() - 1
        qp.setPen(QPen(Qt.black, 2))
        for x in range(0, width, 10):
            if x % 50 == 0 and x > 0:
                qp.drawText(x, 20, str(x))
                qp.setPen(QPen(Qt.red, 3))
                qp.drawLine(x, 0, x, 7)
                qp.setPen(QPen(Qt.black, 2))
            else:
                qp.drawLine(x, 0, x, 5)

        for y in range(0, height, 10):
            if y % 50 == 0 and y > 0:
                qp.drawText(20, y, str(y))
                qp.setPen(QPen(Qt.red, 3))
                qp.drawLine(0, y, 7, y)
                qp.setPen(QPen(Qt.black, 2))
            else:
                qp.drawLine(0, y, 5, y)

    def draw_net(self, qp):
        size = self.size()
        width = size.width() - 1
        height = size.height() - 1
        qp.setPen(QPen(Qt.gray, 1))
        for x in range(0, width, 10):
            qp.drawLine(x, 0, x, height)
        for y in range(0, height, 10):
            qp.drawLine(0, y, width, y)

    def draw_person(self, qp, x, y, vector_angle, vector_len):
        qp.setPen(QPen(Qt.red, 3))
        qp.setBrush(QBrush(Qt.blue, Qt.SolidPattern))

        size = self.size()

        if size.height() <= 1 or size.width() <= 1:
            return
        qp.drawEllipse(x - 3.5, y - 3.5, 7, 7)
        qp.setPen(QPen(Qt.blue, 3))
        future_position_x = x + vector_len * SPEED_SCALE_MULTIPLIER * math.sin(vector_angle)
        future_position_y = y + vector_len * SPEED_SCALE_MULTIPLIER * math.cos(vector_angle)
        qp.drawLine(x,
                    y,
                    future_position_x,
                    future_position_y)

    def draw_wall(self, qp, x_1, y_1, x_2, y_2):
        qp.setPen(QPen(Qt.darkGreen, 2))
        size = self.size()
        qp.drawLine(x_1, y_1, x_2, y_2)



