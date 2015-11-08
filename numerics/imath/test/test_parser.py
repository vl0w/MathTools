import unittest

from numerics.imath.parser import FileParser

test_matrix_path = "./numerics/imath/test/test_matrix.txt"


class TestFileParser(unittest.TestCase):
    def test_number_of_equations(self):
        parser = FileParser(test_matrix_path)
        parser.parse()
        self.assertEqual(parser.numberOfEquations, 3)

    def test_coefficient_matrix(self):
        parser = FileParser(test_matrix_path)
        parser.parse()
        mat = parser.coefficients
        self.assertEqual(mat.size.height, 3)
        self.assertEqual(mat.size.width, 3)
        self.assertEqual(mat.get(1, 1), 2)
        self.assertEqual(mat.get(1, 2), -1)
        self.assertEqual(mat.get(1, 3), 3)
        self.assertEqual(mat.get(2, 1), -4)
        self.assertEqual(mat.get(2, 2), 6)
        self.assertEqual(mat.get(2, 3), -5)
        self.assertEqual(mat.get(3, 1), 6)
        self.assertEqual(mat.get(3, 2), 13)
        self.assertEqual(mat.get(3, 3), 16)

    def test_result_matrix(self):
        parser = FileParser(test_matrix_path)
        parser.parse()
        mat = parser.results
        self.assertEqual(mat.size.height, 3)
        self.assertEqual(mat.size.width, 1)
        self.assertEqual(mat.get(1, 1), 2)
        self.assertEqual(mat.get(2, 1), 1)
        self.assertEqual(mat.get(3, 1), 3)
