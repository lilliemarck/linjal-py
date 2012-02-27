import sys
from PyQt4.QtCore import Qt
from PyQt4.QtGui import (qApp, QApplication, QGraphicsScene, QGraphicsView, QStyle)
from shape import Shape

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 400

def center_widget_on_desktop(widget):
    widget.setGeometry(QStyle.alignedRect(Qt.LeftToRight,
                                          Qt.AlignCenter,
                                          widget.size(),
                                          qApp.desktop().availableGeometry()))


class Canvas(QGraphicsView):
    def __init__(self):
        self._scene = QGraphicsScene()
        QGraphicsView.__init__(self, self._scene)
        self._shape = Shape()

    def mousePressEvent(self, event):
        point = self.mapToScene(event.x(), event.y())
        self._shape.append_point((point.x(), point.y()))
        self._scene.clear()
        self._scene.addPath(self._shape.make_painter_path())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    canvas = Canvas()
    canvas.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    center_widget_on_desktop(canvas)
    canvas.show()

    app.setActiveWindow(canvas) # Fixes some GC issue when closing the window
    app.exec_()
