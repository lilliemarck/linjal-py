import sys
from PyQt4.QtCore import Qt
from PyQt4.QtGui import (qApp, QAction, QActionGroup, QApplication,
                         QGraphicsScene, QGraphicsView, QMainWindow, QStyle)
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
        self._shape.insert_point((point.x(), point.y()))
        self._scene.clear()
        self._scene.addPath(self._shape.make_painter_path())


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setCentralWidget(Canvas())

        select_action = QAction("Select", None)
        select_action.setCheckable(True)
        pen_action = QAction("Pen", None)
        pen_action.setCheckable(True)
        pen_action.setChecked(True)

        self._tool_group = QActionGroup(None)
        self._tool_group.addAction(select_action)
        self._tool_group.addAction(pen_action)

        toolbar = self.addToolBar("Tools")
        toolbar.addAction(select_action)
        toolbar.addAction(pen_action)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    center_widget_on_desktop(main_window)
    main_window.show()

    app.setActiveWindow(main_window) # Fixes some GC issue when closing the window
    app.exec_()
