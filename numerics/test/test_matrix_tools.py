from unittest import TestCase
from numerics.matrix_tools import lu_decomposition, permutate_by_first_pivot
from numerics.matrix import *


class TestSortByFirstPivot(TestCase):
    def test_sort_square_matrix(self):
        permutated = permutate_by_first_pivot(parse_matrix("1 2;3 4"))
        self.assertEqual(parse_matrix("3 4;1 2"), permutated)

    def test_sort_non_square_matrix(self):
        permutated = permutate_by_first_pivot(parse_matrix("1 2;5 6;3 4"))
        self.assertEqual(parse_matrix("5 6;3 4;1 2"), permutated)


class TestLUDecomposition(TestCase):
    def test_upper_triangular_matrix(self):
        a = parse_matrix("1 4;2 12")
        lu = lu_decomposition(a)
        self.assertEqual(parse_matrix("2 12;0 -2"), lu.U)

    def test_lower_triangular_matrix(self):
        a = parse_matrix("1 4;2 12")
        lu = lu_decomposition(a)
        self.assertEqual(parse_matrix("1 0;0.5 1"), lu.L)

    def test_multiply_decomposed_values(self):
        a = parse_matrix("2 12;1 4")
        lu = lu_decomposition(a)
        self.assertEqual(a, lu.L * lu.U)
