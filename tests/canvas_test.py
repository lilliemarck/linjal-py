import unittest
from canvas import MouseEvent, SelectTool
from document import Document

def _perform_click(tool, x, y):
    """Do a mouse press followed by a mouse release."""
    event = MouseEvent((x, y))
    tool.mouse_press_event(event)
    tool.mouse_release_event(event)


class TestSelectTool(unittest.TestCase):
    def testSelectsWhenMouseClicked(self):
        document = Document()
        document.new_shape()
        document.current_shape.append_point((0, 0))
        tool = SelectTool(document)

        self.assertTrue(document.selected_point_index is None)
        _perform_click(tool, 0, 0)
        self.assertTrue(document.selected_point_index == 0)

    def testDeselectsWhenClickingElsewhere(self):
        document = Document()
        document.new_shape()
        document.current_shape.append_point((0, 0))
        tool = SelectTool(document)

        _perform_click(tool, 0, 0)
        _perform_click(tool, 1000, 0) # Click far away
        self.assertTrue(document.selected_point_index is None)


if __name__ == "__main__":
    unittest.main()
