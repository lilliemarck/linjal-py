import sys
from PyQt4.QtCore import Qt
from PyQt4.QtGui import (qApp, QAction, QActionGroup, QApplication,
                         QKeySequence, QMainWindow, QStyle)
from canvas import Canvas, PenTool, SelectTool

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 400

def center_widget_on_desktop(widget):
    widget.setGeometry(QStyle.alignedRect(Qt.LeftToRight,
                                          Qt.AlignCenter,
                                          widget.size(),
                                          qApp.desktop().availableGeometry()))


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self._create_actions()
        self._create_toolbar()
        self._canvas = Canvas()
        self._canvas.scale(16, 16)
        self.setCentralWidget(self._canvas)

    def _create_actions(self):
        self._delete_action = QAction("Delete", None)
        self._delete_action.setShortcuts(QKeySequence.Delete)
        self._delete_action.triggered.connect(self._delete)

        self._select_action = QAction("Select", None)
        self._select_action.setCheckable(True)
        self._select_action.triggered.connect(self._select_select_tool)

        self._pen_action = QAction("Pen", None)
        self._pen_action.setCheckable(True)
        self._pen_action.setChecked(True)
        self._pen_action.triggered.connect(self._select_pen_tool)

        self._new_shape_action = QAction("New Shape", None)
        self._new_shape_action.triggered.connect(self._new_shape)

        self._tool_group = QActionGroup(None)
        self._tool_group.addAction(self._select_action)
        self._tool_group.addAction(self._pen_action)

    def _create_toolbar(self):
        toolbar = self.addToolBar("Tools")
        toolbar.addAction(self._delete_action)
        toolbar.addAction(self._select_action)
        toolbar.addAction(self._pen_action)
        toolbar.addAction(self._new_shape_action)

    def _select_select_tool(self):
        self._canvas.use_tool(SelectTool)

    def _select_pen_tool(self):
        self._canvas.use_tool(PenTool)

    def _new_shape(self):
        self._canvas.new_shape()

    def _delete(self):
        self._canvas.delete_selection()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    center_widget_on_desktop(main_window)
    main_window.show()

    app.setActiveWindow(main_window) # Fixes some GC issue when closing the window
    app.exec_()
