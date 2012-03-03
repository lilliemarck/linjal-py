import math
import sys
from PyQt4.QtGui import QPainterPath

def _vec_add(lhs, rhs):
    return (lhs[0] + rhs[0], lhs[1] + rhs[1])

def _vec_sub(lhs, rhs):
    return (lhs[0] - rhs[0], lhs[1] - rhs[1])

def _vec_scale(v, s):
    return (v[0] * s, v[1] * s)

def _vec_dot(lhs, rhs):
    return (lhs[0] * rhs[0] + lhs[1] * rhs[1])

def _vec_length(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1])

def _vec_distance(lhs, rhs):
    return _vec_length(_vec_sub(lhs, rhs))


def _nearest_point_on_line(begin, end, point):
    """Return the nearest point on the line segment."""
    b2e = _vec_sub(end, begin)
    b2p = _vec_sub(point, begin)
    nom = _vec_dot(b2p, b2e)
    denom = _vec_dot(b2e, b2e)
    if denom == 0.0:
        return begin
    u = nom / denom
    if u <= 0.0:
        return begin
    elif u >= 1.0:
        return end
    else:
        return _vec_add(begin, _vec_scale(b2e, u))


def _distance_to_line(begin, end, point):
    """Return the distance between a line and a point."""
    return _vec_distance(point, _nearest_point_on_line(begin, end, point))


def _insertion_index(points, point):
    """Return the best index for inserting the point."""
    distance = sys.float_info.max
    index = None
    begin = points[-1]
    for i, p in enumerate(points):
        temp = _distance_to_line(begin, p, point)
        if temp < distance:
            distance = temp
            index = i
        begin = p
    return index


def _nearest_point_index(points, point):
    """Return the index of the point nearest to the given point."""
    distance = sys.float_info.max
    index = None
    for i, p in enumerate(points):
        temp = _vec_distance(p, point)
        if temp < distance:
            distance = temp
            index = i
    return index, distance


class Shape:
    """Represents a graphical shape."""

    def __init__(self):
        object.__init__(self)
        self._points = []

    def __getitem__(self, index):
        return self._points[index]

    def __setitem__(self, index, point):
        self._points[index] = point

    def __delitem__(self, index):
        del self._points[index]

    def __len__(self):
        return len(self._points)

    def append_point(self, point):
        """Append a new point to the end of the shape."""
        self._points.append(point)

    def insert_point(self, point):
        """Insert a new point at the best place."""
        points = self._points;
        if len(points) < 3:
            points.append(point)
        else:
            points.insert(_insertion_index(points, point), point)

    def nearest_point_index(self, point):
        """Return the index of the point nearest to the given point."""
        return _nearest_point_index(self._points, point)

    def make_painter_path(self):
        """Return a new QPainterPath used for drawing the shape."""
        path = QPainterPath()
        points = self._points
        if points:
            point = points[0]
            path.moveTo(point[0], point[1])
            for i in range(1, len(self._points)):
                point = points[i]
                path.lineTo(point[0], point[1])
            path.closeSubpath()
        return path;
