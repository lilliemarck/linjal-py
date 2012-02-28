from PyQt4.QtGui import (QGraphicsScene, QGraphicsView)
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
        self.use_tool(PenTool)

    def use_tool(self, tool_class):
        """Instantiates tool_class and uses it as the current tool."""
        self._tool = tool_class(self)

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


class SelectTool:
    """Tool used for selecting points."""
    def __init__(self, canvas):
        pass


class PenTool:
    """Tool used for inserting points."""
    def __init__(self, canvas):
        self._canvas = canvas

    def mouse_press_event(self, event):
        shape = self._canvas.shape
        scene = self._canvas.scene
        shape.insert_point(event.point)
        scene.clear()
        scene.addPath(shape.make_painter_path())
