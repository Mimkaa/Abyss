import pygame as pg
import numpy as np
import random
import math
from numba import njit
from settings import *
vec = pg.Vector2

@njit(fastmath=True)
def get_spline_points(t,arr):

        p1 = int(t)
        p2 = (p1 + 1) % len(arr)
        p3 = (p2 + 1) % len(arr)
        if p1 >= 1:
            p0 = p1 - 1
        else:
            p0 = len(arr) - 1

        t = t - int(t)

        q1 = -t ** 3 + 2 * t ** 2 - t
        q2 = 3 * t ** 3 - 5 * t ** 2 + 2
        q3 = -3 * t ** 3 + 4 * t ** 2 + t
        q4 = t ** 3 - t ** 2

        tx = 0.5 * (arr[p0][0] * q1 + arr[p1][0] * q2 + arr[p2][0] * q3 + arr[
            p3][0] * q4)
        ty = 0.5 * (arr[p0][1] * q1 + arr[p1][1] * q2 + arr[p2][1] * q3 + arr[
            p3][1] * q4)
        return tx, ty

class Outline:
    def __init__(self, width, height, points, pos, angle):
        self.ellipse_points = [vec(v) for v in self.create_ellipse_points(width, height, points, pos, rotation = math.radians(angle))]
        self.ellipse_normals = []
        for i in range(len(self.ellipse_points)):
            dir_vec = (self.ellipse_points[(i + 1) % len(self.ellipse_points)] - self.ellipse_points[i]) * -1
            self.ellipse_normals.append(vec(-dir_vec.y, dir_vec.x))
        self.ellipse_normals_length = [random.randint(10, 50) for i in range(len(self.ellipse_normals))]
        self.ellipse_normals_speed = [random.randint(10, 50) for i in range(len(self.ellipse_normals))]
        self.ellipse_normals_dir = [random.choice([-1, 1]) for i in range(len(self.ellipse_normals))]
        self.ellipse_normals_copy = [v.copy() for v in self.ellipse_normals]



    def create_ellipse_points(self, width, height, number_points, pos,  rotation = 0.):

        right_ellips_points_rotated = []

        el_derivative = lambda x : math.sqrt((width * math.sin(x)) ** 2 + (height * math.cos(x)) ** 2)
        dtheta = 0.0001
        iternum = int((math.pi * 2) / 0.0001)

        # get the circumference by integrating over the ellipse
        circumference = sum([el_derivative(i * dtheta) for i in range(iternum)])

        # creating the points
        next_point = 0
        has_run = 0.
        theta = 0.
        for i in range(iternum):
            theta += dtheta
            current_point = (number_points * has_run) / circumference
            if current_point > next_point:
                x = width * math.cos(theta)
                y = height * math.sin(theta)
                # rotation and offset
                x = x * math.cos(rotation) - y * math.sin(rotation) + pos[0]
                y = x * math.sin(rotation) + y * math.cos(rotation) + pos[1]
                next_point += 1
                right_ellips_points_rotated.append([x, y])
            has_run += el_derivative(theta)
        return right_ellips_points_rotated

    def update(self, dt):
        for n, v in enumerate(self.ellipse_normals):
            if v.length() >= self.ellipse_normals_length[n]:
                self.ellipse_normals_dir[n] *= -1
                v.scale_to_length(self.ellipse_normals_length[n])

            move_vec = self.ellipse_normals_copy[n].copy()
            move_vec.scale_to_length(self.ellipse_normals_speed[n] * dt)
            move_vec *= self.ellipse_normals_dir[n]
            v += move_vec

    def draw(self, surf):
        arr = list(np.arange(0.0, len(self.ellipse_normals), 0.3))
        poly_points = []
        points_offseted = [self.ellipse_points[n].copy() + self.ellipse_normals[n].copy() for n in range(len(self.ellipse_points))]
        points_offseted = np.array([tuple(v) for v in points_offseted])
        for t in arr:
            poly_points.append(vec(get_spline_points(t, points_offseted)))

        pg.draw.polygon(surf, WHITE, poly_points)