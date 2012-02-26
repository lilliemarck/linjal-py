import sys
from PyQt4.QtCore import Qt
from PyQt4.QtGui import (qApp, QApplication, QGraphicsScene, QGraphicsView,
                         QPainterPath, QStyle)

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
        self._path = None
        
    def mousePressEvent(self, event):
        point = self.mapToScene(event.x(), event.y())
        x, y = point.x(), point.y()

        if self._path:
            self._path.lineTo(x, y)
        else:            
            self._path = QPainterPath()
            self._path.moveTo(x, y)

        self._scene.clear()
        self._scene.addPath(self._path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    canvas = Canvas()
    canvas.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    center_widget_on_desktop(canvas)
    canvas.show()

    app.setActiveWindow(canvas) # Fixes some GC issue when closing the window
    app.exec_()
