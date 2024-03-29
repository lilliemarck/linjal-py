import unittest
from document import Document, Shape

class TestShape(unittest.TestCase):
    def test_path_from_empty_shape(self):
        shape = Shape()
        path = shape.make_painter_path()
        self.assertEqual(path.length(), 0)

    def test_path_from_shape_with_one_point(self):
        shape = Shape()
        shape.append_point((10, 20))
        path = shape.make_painter_path()
        self.assertEqual(1, path.elementCount())

        element = path.elementAt(0)
        self.assertTrue(element.isMoveTo())
        self.assertEquals(element.x, 10)
        self.assertEqual(element.y, 20)

    def test_path_from_shape_with_two_points(self):
        shape = Shape()
        shape.append_point((10, 20))
        shape.append_point((30, 40))
        path = shape.make_painter_path()
        self.assertEqual(3, path.elementCount())

        element = path.elementAt(0)
        self.assertTrue(element.isMoveTo())
        self.assertEquals(element.x, 10)
        self.assertEqual(element.y, 20)

        element = path.elementAt(1)
        self.assertTrue(element.isLineTo())
        self.assertEquals(element.x, 30)
        self.assertEqual(element.y, 40)

        element = path.elementAt(2)
        self.assertTrue(element.isLineTo())
        self.assertEquals(element.x, 10)
        self.assertEqual(element.y, 20)

    def test_path_from_shape_with_three_points(self):
        shape = Shape()
        shape.append_point((10, 20))
        shape.append_point((30, 40))
        shape.append_point((50, 60))
        path = shape.make_painter_path()
        self.assertEqual(4, path.elementCount())

        element = path.elementAt(0)
        self.assertTrue(element.isMoveTo())
        self.assertEquals(element.x, 10)
        self.assertEqual(element.y, 20)

        element = path.elementAt(1)
        self.assertTrue(element.isLineTo())
        self.assertEquals(element.x, 30)
        self.assertEqual(element.y, 40)

        element = path.elementAt(2)
        self.assertTrue(element.isLineTo())
        self.assertEquals(element.x, 50)
        self.assertEqual(element.y, 60)

        element = path.elementAt(3)
        self.assertTrue(element.isLineTo())
        self.assertEquals(element.x, 10)
        self.assertEqual(element.y, 20)


class TestDocument(unittest.TestCase):
    def testNewDocuentHasNoShapes(self):
        document = Document()
        self.assertEqual(document.shape_count, 0)

    def testNewShape(self):
        document = Document()
        shape = document.new_shape()
        self.assertTrue(shape is not None)
        self.assertEqual(document.shape_count, 1)

    def testRedundantNewShapeCreatesOnlyOneShape(self):
        document = Document()
        document.new_shape()
        document.new_shape()
        self.assertEqual(document.shape_count, 1)


if __name__ == "__main__":
    unittest.main()
