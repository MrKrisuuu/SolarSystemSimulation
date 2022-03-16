import ephem
import numpy as np
from PyQt5.QtGui import QColor
from datetime import datetime, timedelta
from Body import *

SUN_MASS = 1.989e30
MERCURY_MASS = 3.301e23
VENUS_MASS = 4.867e24
EARTH_MASS = 5.972e24
MARS_MASS = 6.417e23
JUPITER_MASS = 1.898e27
SATURN_MASS = 5.683e26
URANUS_MASS = 8.681e25
NEPTUNE_MASS = 1.024e26

SUN_COLOR = QColor(255, 255, 0)
MERCURY_COLOR = QColor(146, 137, 138)
VENUS_COLOR = QColor(206, 204, 196)
EARTH_COLOR = QColor(0, 0, 255)
MARS_COLOR = QColor(227, 106, 77)
JUPITER_COLOR = QColor(153, 96, 79)
SATURN_COLOR = QColor(235, 201, 130)
URANUS_COLOR = QColor(207, 245, 246)
NEPTUNE_COLOR = QColor(66, 108, 252)

SUN_RADIUS = 696340000
MERCURY_RADIUS = 2439000
VENUS_RADIUS = 6051000
EARTH_RADIUS = 6378000
MARS_RADIUS = 3396000
JUPITER_RADIUS = 71492000
SATURN_RADIUS = 60268000
URANUS_RADIUS = 25559000
NEPTUNE_RADIUS = 24764000


def new_body(planet, mass, color, size, radius):
    seconds = 10000
    planet.compute(datetime.now())
    if planet.sun_distance == 0:
        x = np.cos(planet.hlon) * ephem.meters_per_au
        y = np.sin(planet.hlon) * ephem.meters_per_au
    else:
        x = np.cos(planet.hlon) * planet.sun_distance * ephem.meters_per_au
        y = np.sin(planet.hlon) * planet.sun_distance * ephem.meters_per_au
    planet.compute(datetime.now() + timedelta(seconds=seconds))
    if planet.sun_distance == 0:
        x_1 = np.cos(planet.hlon) * ephem.meters_per_au
        y_1 = np.sin(planet.hlon) * ephem.meters_per_au
    else:
        x_1 = np.cos(planet.hlon) * planet.sun_distance * ephem.meters_per_au
        y_1 = np.sin(planet.hlon) * planet.sun_distance * ephem.meters_per_au
    return Body(mass=mass,
                radius=radius,
                size=size,
                x=x,
                y=y,
                x_velocity=(x_1-x) / seconds,
                y_velocity=(y_1-y) / seconds,
                color=color)


def create_solar_system():
    space = []
    space.append(Body(mass=SUN_MASS, radius=SUN_RADIUS, size=15, color=SUN_COLOR))
    space.append(new_body(ephem.Mercury(), MERCURY_MASS, MERCURY_COLOR, 3, MERCURY_RADIUS))
    space.append(new_body(ephem.Venus(), VENUS_MASS, VENUS_COLOR, 5, VENUS_RADIUS))
    space.append(new_body(ephem.Sun(), EARTH_MASS, EARTH_COLOR, 5, EARTH_RADIUS))  # Earth
    space.append(new_body(ephem.Mars(), MARS_MASS, MARS_COLOR, 4, MARS_RADIUS))
    space.append(new_body(ephem.Jupiter(), JUPITER_MASS, JUPITER_COLOR, 10, JUPITER_RADIUS))
    space.append(new_body(ephem.Saturn(), SATURN_MASS, SATURN_COLOR, 9, SATURN_RADIUS))
    space.append(new_body(ephem.Uranus(), URANUS_MASS, URANUS_COLOR, 7, URANUS_RADIUS))
    space.append(new_body(ephem.Neptune(), NEPTUNE_MASS, NEPTUNE_COLOR, 7, NEPTUNE_RADIUS))
    return space
