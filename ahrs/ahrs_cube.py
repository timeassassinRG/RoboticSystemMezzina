import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import time
import math

from imu_driver import IMUDriver
from comp_filter import ComplementaryAHRSFilter

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)


def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def main():
    pygame.init()
    (width, height) = (800, 600)
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()
    gluPerspective(20, width / float(height), 5, 15)
    glViewport(0, 0, width, height)

    glMatrixMode(GL_MODELVIEW)

    imu = IMUDriver()

    imu.open()

    filt = ComplementaryAHRSFilter(1.0, 0.02)

    last_t = time.time()

    glMatrixMode(GL_MODELVIEW)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        imu_data = imu.sample()
        t = time.time()
        delta_t = t - last_t
        filt.update(delta_t,
                    imu_data[0], imu_data[1], imu_data[2],
                    imu_data[3], imu_data[4], imu_data[5])
        last_t = t
        (r, p) = filt.get_attitude()

        # glTranslatef(0, 0, -100);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -10)
        glRotatef(-math.degrees(p), 0, 0, 1)
        glRotatef(math.degrees(r), 1, 0, 0)
        Cube()
        pygame.display.flip()
        # pygame.time.wait(10)


main()
