import unittest

from numerics.matrix import Dim, create_matrix, create_square_matrix, create_identity_matrix, parse_matrix


class TestDimension(unittest.TestCase):
    def test_different_length_and_width(self):
        dim = Dim(2, 3)
        self.assertEqual(dim.height, 2)
        self.assertEqual(dim.width, 3)

    def test_squared_dimension(self):
        dim = Dim(2)
        self.assertEqual(dim.height, 2)
        self.assertEqual(dim.width, 2)


class TestMatrix(unittest.TestCase):
    def test_initialized_with_zero(self):
        m = create_square_matrix(3)

        def check_is_zero(row, column, value): self.assertEqual(0, value)

        m.on_every_element(check_is_zero)

    def test_set_values(self):
        m = create_square_matrix(2)
        m.set(1, 1, 1)
        m.set(1, 2, 2)
        m.set(2, 1, 3)
        m.set(2, 2, 4)

        self.assertEqual(m.get(1, 1), 1)
        self.assertEqual(m.get(1, 2), 2)
        self.assertEqual(m.get(2, 1), 3)
        self.assertEqual(m.get(2, 2), 4)

    def test_get_with_index_below_one(self):
        self.assertRaises(ValueError, create_square_matrix(2).get, 0, 1)
        self.assertRaises(ValueError, create_square_matrix(2).get, 1, 0)
        self.assertRaises(ValueError, create_square_matrix(2).get, 0, 0)

    def test_get_with_index_above_size(self):
        self.assertRaises(ValueError, create_square_matrix(2).get, 3, 1)
        self.assertRaises(ValueError, create_square_matrix(2).get, 1, 3)
        self.assertRaises(ValueError, create_square_matrix(2).get, 3, 3)

    def test_set_with_index_below_one(self):
        self.assertRaises(ValueError, create_square_matrix(2).set, 0, 1, -1)
        self.assertRaises(ValueError, create_square_matrix(2).set, 1, 0, -1)
        self.assertRaises(ValueError, create_square_matrix(2).set, 0, 0, -1)

    def test_set_with_index_above_size(self):
        self.assertRaises(ValueError, create_square_matrix(2).set, 3, 1, -1)
        self.assertRaises(ValueError, create_square_matrix(2).set, 1, 3, -1)
        self.assertRaises(ValueError, create_square_matrix(2).set, 3, 3, -1)

    def test_append_row_with_wrong_width(self):
        m = create_square_matrix(2)
        self.assertRaises(ValueError, m.append_row, [1, 2, 3])

    def test_get_row(self):
        self.assertEqual(parse_matrix("3 4"), parse_matrix("1 2;3 4").get_row(2))

    def test_get_column(self):
        self.assertEqual(parse_matrix("2;4"), parse_matrix("1 2;3 4").get_column(2))

    def test_append_row(self):
        m = create_square_matrix(2)
        m.append_row([1, 2])
        self.assertEqual(m.size.height, 3)
        self.assertEqual(m.size.width, 2)
        self.assertEqual(m.get(3, 1), 1)
        self.assertEqual(m.get(3, 2), 2)

    def test_append_row_to_empty_matrix(self):
        m = create_matrix(0, 0)
        m.append_row([1, 2])

        self.assertEqual(m.size.height, 1)
        self.assertEqual(m.size.width, 2)
        self.assertEqual(m.get(1, 1), 1)
        self.assertEqual(m.get(1, 2), 2)

    def test_append_column_with_wrong_height(self):
        m = create_square_matrix(2)
        self.assertRaises(ValueError, m.append_column, parse_matrix("1;2;3"))

    def test_append_column(self):
        m = create_square_matrix(2)
        m.append_column(parse_matrix("1 2").transpose())
        self.assertEqual(m.size.height, 2)
        self.assertEqual(m.size.width, 3)
        self.assertEqual(m.get(1, 3), 1)
        self.assertEqual(m.get(2, 3), 2)

    def test_append_column_to_empty_matrix(self):
        m = create_matrix(0, 0)
        m.append_column(parse_matrix("1;2"))

        self.assertEqual(m.size.height, 2)
        self.assertEqual(m.size.width, 1)
        self.assertEqual(m.get(1, 1), 1)
        self.assertEqual(m.get(2, 1), 2)

    def test_equality(self):
        a = parse_matrix("1 2;3 4")
        b = parse_matrix("1 2;3 4")
        self.assertEqual(a, b)

    def test_inequality(self):
        self.assertNotEqual(parse_matrix("1 2;3 4"), parse_matrix("1 2;3 5"))
        self.assertNotEqual(parse_matrix("1 2;3 4"), parse_matrix("1 2 3;4 5 6"))

    def test_exchange_rows(self):
        a = parse_matrix("1 2;3 4;5 6")
        a.exchange_rows(1, 3)
        self.assertEqual(parse_matrix("5 6;3 4;1 2"), a)

    def test_copy(self):
        a = parse_matrix("1 2;3 4")
        b = a.copy()
        self.assertEqual(b, a)

        b.set(1, 1, 3)
        self.assertNotEqual(b, a)

    def test_is_square(self):
        self.assertTrue(parse_matrix("1 2;3 4").is_square())
        self.assertFalse(parse_matrix("1 2 3;4 5 6").is_square())

    def test_upper_triangle(self):
        a = parse_matrix("1 2 3;4 5 6;7 8 9")
        expected_matrix = parse_matrix("0 2 3;0 0 6;0 0 0")
        self.assertEqual(expected_matrix, a.upper_triangle())

    def test_lower_triangle(self):
        a = parse_matrix("1 2 3;4 5 6;7 8 9")
        expected_matrix = parse_matrix("0 0 0;4 0 0;7 8 0")
        self.assertEqual(expected_matrix, a.lower_triangle())

    def test_diagonal_matrix(self):
        a = parse_matrix("1 2 3;4 5 6;7 8 9")
        expected_matrix = parse_matrix("1 0 0;0 5 0;0 0 9")
        self.assertEqual(expected_matrix, a.diagonal_matrix())

class TestMatrixFactories(unittest.TestCase):
    def test_parse_1x1_matrix(self):
        m = parse_matrix("5")

        self.assertEqual(m.size.height, 1)
        self.assertEqual(m.size.width, 1)
        self.assertEqual(m.get(1, 1), 5)

    def test_parse_1x3_matrix(self):
        m = parse_matrix("5 4 3")

        self.assertEqual(m.size.height, 1)
        self.assertEqual(m.size.width, 3)
        self.assertEqual(m.get(1, 1), 5)
        self.assertEqual(m.get(1, 2), 4)
        self.assertEqual(m.get(1, 3), 3)

    def test_parse_2x2_matrix(self):
        m = parse_matrix("1 2;3 4")

        self.assertEqual(m.size.height, 2)
        self.assertEqual(m.size.width, 2)
        self.assertEqual(m.get(1, 1), 1)
        self.assertEqual(m.get(1, 2), 2)
        self.assertEqual(m.get(2, 1), 3)
        self.assertEqual(m.get(2, 2), 4)

    def test_parse_with_invalid_matrix_definition(self):
        self.assertRaises(ValueError, parse_matrix, "1 2;1")
        self.assertRaises(ValueError, parse_matrix, "1 2/1 2")
        self.assertRaises(ValueError, parse_matrix, "1 a;1 2")
        self.assertRaises(ValueError, parse_matrix, "[1 2];[1 2]")

    def test_create_identity_matrix(self):
        m = create_identity_matrix(2);

        self.assertEqual(m.size.height, 2)
        self.assertEqual(m.size.width, 2)
        self.assertEqual(m.get(1, 1), 1)
        self.assertEqual(m.get(1, 2), 0)
        self.assertEqual(m.get(2, 1), 0)
        self.assertEqual(m.get(2, 2), 1)


class TestMatrixArithmetic(unittest.TestCase):
    def test_addition(self):
        # a+b=c
        a = parse_matrix("1 2;3 4")
        b = parse_matrix("5 6;7 8")
        c = parse_matrix("6 8;10 12")
        self.assertEqual(c, a + b)

    def test_addition_commutative_law(self):
        # a+b=b+a
        a = parse_matrix("1 2;3 4")
        b = parse_matrix("5 6;7 8")
        self.assertEqual(a + b, b + a)

    def test_addition_with_invalid_type(self):
        # addition with scalar is invalid
        def add():
            parse_matrix("1 2;3 4") + 5

        self.assertRaises(ValueError, add)

    def test_addition_invalid_dimensions(self):
        def add():
            parse_matrix("1 2;3 4") + parse_matrix("1 2 3;4 5 6")

        self.assertRaises(ArithmeticError, add)

    def test_subtraction_from_right(self):
        # a-b=c
        a = parse_matrix("1 2;3 4")
        b = parse_matrix("5 6;7 8")
        c = parse_matrix("-4 -4;-4 -4")
        self.assertEqual(c, a - b)

    def test_subtraction_from_left(self):
        # b-a=c
        b = parse_matrix("5 6;7 8")
        a = parse_matrix("1 2;3 4")
        c = parse_matrix("4 4;4 4")
        self.assertEqual(c, b - a)

    def test_subtraction_is_not_commutative(self):
        # a-b!=b-a
        a = parse_matrix("1 2;3 4")
        b = parse_matrix("5 6;7 8")
        self.assertNotEqual(a - b, b - a)

    def test_subtraction_with_invalid_type(self):
        # subtraction with scalar is invalid
        def sub():
            parse_matrix("1 2;3 4") - 5

        self.assertRaises(ValueError, sub)

    def test_subtraction_invalid_dimensions(self):
        def sub():
            parse_matrix("1 2;3 4") - parse_matrix("1 2 3;4 5 6")

        self.assertRaises(ArithmeticError, sub)

    def test_transpose_row(self):
        self.assertEqual(parse_matrix("1;2;3"), parse_matrix("1 2 3").transpose())

    def test_1xn_nx1_multiplication(self):
        a = parse_matrix("1 2 3")
        b = parse_matrix("4 5 6").transpose()
        c = parse_matrix("32")
        self.assertEqual(c, a * b)

    def test_mxn_nxm_multiplication(self):
        a = parse_matrix("1 2;3 4")
        b = parse_matrix("5 6;7 8")
        c = parse_matrix("19 22;43 50")
        self.assertEqual(c, a * b)

    def test_axn_nxb_multiplication(self):
        a = parse_matrix("1 2 3;4 5 6")
        b = parse_matrix("7 8 9 10;11 12 13 14;15 16 17 18")
        c = parse_matrix("74 80 86 92;173 188 203 218")
        self.assertEqual(c, a * b)

    def test_multiplication_invalid_dimensions(self):
        def multiply():
            parse_matrix("1 2 3") * parse_matrix("1 2 3")

        self.assertRaises(ArithmeticError, multiply)

    def test_multiplication_commutative_law(self):
        a = parse_matrix("1 2;3 4")
        b = parse_matrix("5 6;7 8")
        self.assertNotEqual(a * b, b * a)

    def test_multiplication_with_scalar(self):
        a = parse_matrix("1 2;3 4")
        self.assertEqual(parse_matrix("5 10;15 20"), a * 5)

    def test_multiplication_with_scalar_commutative_law(self):
        a = parse_matrix("1 2;3 4")
        self.assertEqual(a * 5, 5 * a)

    def test_multiplication_with_invalid_type(self):
        def multiply():
            parse_matrix("1") * "2"

        self.assertRaises(ValueError, multiply)

    def test_multiplication_with_identity_matrix(self):
        # a * I = a
        a = parse_matrix("1 2 3;4 5 6;7 8 9")
        I = create_identity_matrix(3)
        self.assertEqual(a, a * I)
        self.assertEqual(a, I * a)
