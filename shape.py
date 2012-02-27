from PyQt4.QtGui import QPainterPath

class Shape:
    """Represents a graphical shape."""

    def __init__(self):
        object.__init__(self)
        self._points = []

    def append_point(self, point):
        """Append a new point to the shape."""
        self._points.append(point)

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
