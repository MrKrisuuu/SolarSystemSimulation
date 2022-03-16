import numpy as np
import copy
from PyQt5.QtGui import QColor


G = 6.6743e-11  # stała grawitacji


class Body:
    def __init__(self, mass=1, radius=1, size=10, x=0, y=0, z=0, x_velocity=0, y_velocity=0, z_velocity=0, color=QColor(255, 255, 255)):
        self.mass = mass
        self.radius = radius
        self.size = size
        self.x = x
        self.y = y
        self.z = z
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.z_velocity = z_velocity
        self.color = color

    def r_vector(self, other):  # distance vector from self to other
        r_x = other.x - self.x
        r_y = other.y - self.y
        r_z = other.z - self.z
        return np.array([r_x, r_y, r_z])

    def calculate_force(self, space):
        F = [0, 0, 0]
        for body in space:
            if body != self:
                r = self.r_vector(body)
                F += (G * body.mass * self.mass * r) / np.linalg.norm(r) ** 3
        return F

    def update_speed(self, F, step):
        self.x_velocity += (F[0] * step) / self.mass
        self.y_velocity += (F[1] * step) / self.mass
        self.z_velocity += (F[2] * step) / self.mass

    def update_position(self, step):
        self.x += self.x_velocity * step
        self.y += self.y_velocity * step
        self.z += self.z_velocity * step
        return [self.x, self.y, self.z]


def merge_bodies(body1, body2):
    x = (body1.x * body1.mass + body2.x * body2.mass) / (body1.mass + body2.mass)
    y = (body1.y * body1.mass + body2.y * body2.mass) / (body1.mass + body2.mass)
    x_velocity = (body1.x_velocity * body1.mass + body2.x_velocity * body2.mass) / (body1.mass + body2.mass)
    y_velocity = (body1.y_velocity * body1.mass + body2.y_velocity * body2.mass) / (body1.mass + body2.mass)
    if body1.mass > body2.mass:
        color = body1.color
    else:
        color = body2.color
    return Body(
        mass=(body1.mass+body2.mass),
        size=max(body1.size, body2.size),
        x=x,
        y=y,
        x_velocity=x_velocity,
        y_velocity=y_velocity,
        color=color
    )


def merge_space(space):
    safety_merge = 10
    for body1 in space:
        for body2 in space:
            if body1 != body2:
                if np.linalg.norm(body1.r_vector(body2)) <= safety_merge * (body1.radius + body2.radius):
                    space.remove(body1)
                    space.remove(body2)
                    space.append(merge_bodies(body1, body2))
                    return True
    return False

