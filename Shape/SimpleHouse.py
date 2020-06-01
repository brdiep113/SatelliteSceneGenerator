import shapely.geometry
import shapely.affinity
import numpy as np
import random


class RotatedRect:

    def __init__(self, cx, cy, w, h, angle):
        self.cx = cx
        self.cy = cy
        self.w = w
        self.h = h
        self.angle = angle
        self.center = np.array((cx, cy))

        c = shapely.geometry.box(-w / 2.0, -h / 2.0, w / 2.0, h / 2.0)
        rc = shapely.affinity.rotate(c, self.angle, origin='centroid')
        rce = shapely.affinity.translate(rc, self.cx, self.cy)
        exterior_points = rce.exterior.coords.xy
        self.vertices = self.read_vertices(exterior_points)

        # To be removed
        center = np.array((cx, cy))
        corner_a = np.array((cx + (w / 2), cy + (h / 2)))
        corner_b = np.array((cx + (w / 2), cy - (h / 2)))
        corner_c = np.array((cx - (w / 2), cy - (h / 2)))
        corner_d = np.array((cx - (w / 2), cy + (h / 2)))
        self.matrix = np.array((center, corner_a, corner_b, corner_c, corner_d))

    def rotate(self, theta: float) -> None:
        cos, sin = np.cos(theta), np.sin(theta)
        rotation_matrix = np.array(((cos, -sin), (sin, cos)))
        self.matrix = np.dot(self.matrix, rotation_matrix)

    def read_vertices(self, poly_points):

        # duplicate point
        x_list = poly_points[0]
        y_list = poly_points[1]

        return np.array((x_list, y_list))

    def shift_shape(self, x, y):
        vector = np.array((x, y))
        self.cx += x
        self.cy += y
        self.matrix += vector

    def offset_center(self, vector):
        self.center += vector

    def get_contour(self):
        w = self.w
        h = self.h
        c = shapely.geometry.box(-w / 2.0 - 5, -h / 2.0 - 5, w / 2.0 + 5, h / 2.0 + 5)
        rc = shapely.affinity.rotate(c, self.angle, origin='centroid')
        return shapely.affinity.translate(rc, self.cx, self.cy)

    def intersection(self, other):
        return self.get_contour().intersection(other.get_contour())