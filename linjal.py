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
        self._canvas = Canvas()
        self.setCentralWidget(self._canvas)

        self.delete_action = QAction("Delete", None)
        self.delete_action.setShortcuts(QKeySequence.Delete)
        select_action = QAction("Select", None)
        select_action.setCheckable(True)
        pen_action = QAction("Pen", None)
        pen_action.setCheckable(True)
        pen_action.setChecked(True)

        self._tool_group = QActionGroup(None)
        self._tool_group.addAction(select_action)
        self._tool_group.addAction(pen_action)

        select_action.triggered.connect(self._select_select_tool)
        pen_action.triggered.connect(self._select_pen_tool)
        self.delete_action.triggered.connect(self._delete)

        toolbar = self.addToolBar("Tools")
        toolbar.addAction(self.delete_action)
        toolbar.addAction(select_action)
        toolbar.addAction(pen_action)

    def _select_select_tool(self):
        self._canvas.use_tool(SelectTool)

    def _select_pen_tool(self):
        self._canvas.use_tool(PenTool)

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
