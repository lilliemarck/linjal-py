from PyQt4.QtGui import (QGraphicsScene, QGraphicsView, QPainter)
from shape import Shape

def _round_to_half(value):
    return round(value * 2) // 2


class MouseEvent:
    """A mouse event given in scene space."""
    def __init__(self, point):
        self.point = point


class Canvas(QGraphicsView):
    def __init__(self):
        self._scene = QGraphicsScene()
        QGraphicsView.__init__(self, self._scene)
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
        self._scene.clear()
        self._scene.addPath(self.shape.make_painter_path())

    def _call_tool(self, method_name, *args):
        method = getattr(self._tool, method_name, None)
        if method:
            method(*args)

    def _map_event(self, qt_event):
        """Take a QMouseEvent and return a MouseEvent in scene space."""
        point = self.mapToScene(qt_event.x(), qt_event.y())
        return MouseEvent((_round_to_half(point.x()),
                           _round_to_half(point.y())))

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

    _IDLE_STATE = 0
    _MOVE_STATE = 1
    _KNOB_RADIUS = 2

    def __init__(self, canvas):
        self._canvas = canvas
        self._state = SelectTool._IDLE_STATE
        self._distance = None

    def mouse_move_event(self, event):
        canvas = self._canvas
        shape = canvas.shape

        if self._state == SelectTool._IDLE_STATE:
            if shape:
                index, distance = shape.nearest_point_index(event.point)
                self._distance = distance
                canvas.selection = index
            else:
                self._distance = None
                canvas.selection = None

        elif self._state == SelectTool._MOVE_STATE and canvas.selection is not None:
            shape[canvas.selection] = event.point
            canvas.refresh_scene()

        canvas.update()

    def mouse_press_event(self, event):
        distance = self._distance
        if distance is not None and distance <= SelectTool._KNOB_RADIUS:
            self._state = SelectTool._MOVE_STATE

    def mouse_release_event(self, event):
        self._state = SelectTool._IDLE_STATE

    def paint_event(self, device):
        canvas = self._canvas
        index = canvas.selection
        if index != None:
            point = canvas.shape[index]
            point = canvas.mapFromScene(point[0], point[1])
            painter = QPainter(device)
            painter.drawArc(point.x() - SelectTool._KNOB_RADIUS,
                            point.y() - SelectTool._KNOB_RADIUS,
                            2 * SelectTool._KNOB_RADIUS,
                            2 * SelectTool._KNOB_RADIUS,
                            0,
                            5760)


class PenTool:
    """Tool used for inserting points."""
    def __init__(self, canvas):
        self._canvas = canvas

    def mouse_press_event(self, event):
        canvas = self._canvas
        canvas.shape.insert_point(event.point)
        canvas.refresh_scene()
