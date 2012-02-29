from PyQt4.QtGui import (QGraphicsScene, QGraphicsView, QPainter)
from shape import Shape

class MouseEvent:
    """A mouse event given in scene space."""
    def __init__(self, point):
        self.point = point


class Canvas(QGraphicsView):
    def __init__(self):
        self.scene = QGraphicsScene()
        QGraphicsView.__init__(self, self.scene)
        self.shape = Shape()
        self.selection = None
        self.use_tool(PenTool)
        self.setMouseTracking(True)

    def use_tool(self, tool_class):
        """Instantiates tool_class and uses it as the current tool."""
        self._tool = tool_class(self)

    def delete_selection(self):
        if self.selection is not None:
            del self.shape[self.selection]
            self.selection = None
            self.refresh_scene()

    def refresh_scene(self):
        self.scene.clear()
        self.scene.addPath(self.shape.make_painter_path())

    def _call_tool(self, method_name, *args):
        method = getattr(self._tool, method_name, None)
        if method:
            method(*args)

    def _map_event(self, qt_event):
        """Take a QMouseEvent and return a MouseEvent in scene space."""
        point = self.mapToScene(qt_event.x(), qt_event.y())
        return MouseEvent((point.x(), point.y()))

    def mouseMoveEvent(self, event):
        self._call_tool('mouse_move_event', self._map_event(event))

    def mousePressEvent(self, event):
        self._call_tool('mouse_press_event', self._map_event(event))

    def mouseReleaseEvent(self, event):
        self._call_tool('mouse_release_event', self._map_event(event))

    def paintEvent(self, event):
        QGraphicsView.paintEvent(self, event)
        v = self.viewport()
        self._call_tool('paint_event', v)


class SelectTool:
    """Tool used for selecting points."""
    def __init__(self, canvas):
        self._canvas = canvas

    def mouse_move_event(self, event):
        canvas = self._canvas
        shape = canvas.shape
        if shape:
            canvas.selection = shape.nearest_point_index(event.point)
        else:
            canvas.selection = None
        canvas.update()

    def paint_event(self, device):
        canvas = self._canvas
        index = canvas.selection
        if index != None:
            point = canvas.shape[index]
            point = canvas.mapFromScene(point[0], point[1])
            painter = QPainter(device)
            painter.drawArc(point.x() - 1, point.y() - 1, 3, 3, 0, 5760)


class PenTool:
    """Tool used for inserting points."""
    def __init__(self, canvas):
        self._canvas = canvas

    def mouse_press_event(self, event):
        canvas = self._canvas
        canvas.shape.insert_point(event.point)
        canvas.refresh_scene()
