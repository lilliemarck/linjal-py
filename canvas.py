from PyQt4.QtGui import (QGraphicsScene, QGraphicsView, QPainter)
from document import Document
from signals import Signal

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
        self._document = Document()
        self._document.changed.connect(self._update_scene)
        self.use_tool(PenTool)
        self.setMouseTracking(True)

    def use_tool(self, tool_class):
        """Instantiates tool_class and uses it as the current tool."""
        self._tool = tool_class(self._document)
        self._tool.needs_repaint.connect(self._update)

    def new_shape(self):
        self._document.new_shape()

    def delete_selection(self):
        self._document.delete_selection()
        if not self._document.current_shape:
            self._document.delete_current_shape();

    def _update(self):
        self.update()

    def _update_scene(self):
        self._scene.clear()
        for shape in self._document.shapes:
            self._scene.addPath(shape.make_painter_path())

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
        self._call_tool('paint_event', self)


class Tool:
    """Base class for tools."""

    def __init__(self, document):
        self.needs_repaint = Signal()
        self.document = document


class SelectTool(Tool):
    """Tool used for selecting points."""

    _KNOB_RADIUS = 2

    def __init__(self, document):
        Tool.__init__(self, document)
        self._dragging = False

    def mouse_move_event(self, event):
        document = self.document
        shape = document.current_shape

        if self._dragging and document.selected_point_index is not None:
            shape[document.selected_point_index] = event.point
            document.changed()
            self.needs_repaint()

    def mouse_press_event(self, event):
        document = self.document
        shape = document.current_shape

        if shape:
            index, distance = shape.nearest_point_index(event.point)
            if distance <= SelectTool._KNOB_RADIUS:
                self._dragging = True
                document.selected_point_index = index
            else:
                document.selected_point_index = None
            self.needs_repaint()

    def mouse_release_event(self, event):
        self._dragging = False

    def paint_event(self, canvas):
        document = self.document
        index = document.selected_point_index
        if index != None:
            point = document.current_shape[index]
            point = canvas.mapFromScene(point[0], point[1])
            painter = QPainter(canvas.viewport())
            painter.drawArc(point.x() - SelectTool._KNOB_RADIUS,
                            point.y() - SelectTool._KNOB_RADIUS,
                            2 * SelectTool._KNOB_RADIUS,
                            2 * SelectTool._KNOB_RADIUS,
                            0,
                            5760)


class PenTool(Tool):
    """Tool used for inserting points."""

    def mouse_press_event(self, event):
        document = self.document
        if document.current_shape is not None:
            document.current_shape.insert_point(event.point)
            document.changed()
