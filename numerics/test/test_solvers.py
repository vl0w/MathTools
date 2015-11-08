from unittest import TestCase
from numerics.solvers import *


class TestGaussianElimination(TestCase):
    def test_with_3x3_matrix(self):
        c = parse_matrix("0 8 2;3 5 2;6 2 8")
        b = parse_matrix("-7 8 26").transpose()
        x = gaussian_elimination(c, b)
        self.assertEqual(parse_matrix("4;-1;0.5"), x)
        self.assertEqual(b, c * x)

    def test_with_4x4_matrix(self):
        c = parse_matrix("5 -5 0 0;-5 7 -2 0;0 -2 20 -18;0 0 -18 19")
        b = parse_matrix("5 -7 20 -17").transpose()
        x = gaussian_elimination(c, b)
        self.assertEqual(parse_matrix("2;1;2;1"), x)
        self.assertEqual(b, c * x)


class TestInverseCalculation(TestCase):
    def test_no_square_matrix(self):
        def do():
            inv(parse_matrix("1 2 3;4 5 6"))

        self.assertRaises(ValueError, do)

    def test_calculate_inverse(self):
        a = parse_matrix("3 0;0 1")
        self.assertEqual(create_identity_matrix(2), a * inv(a))
        self.assertEqual(create_identity_matrix(2), inv(a) * a)


class TestGaussSeidelAlgorithm(TestCase):
    def test_with_2x2_matrix(self):
        c = parse_matrix("4 2;0 1")
        b = parse_matrix("4 1").transpose()
        x = gauss_seidel_iteration(c, b)
        self.assertEqual(parse_matrix("0.5;1"), x)

class TestJacobiAlgorithm(TestCase):
    def test_with_2x2_matrix(self):
        c = parse_matrix("4 2;0 1")
        b = parse_matrix("4 1").transpose()
        x = jacobi_iteration(c, b)
        self.assertEqual(parse_matrix("0.5;1"), x)
