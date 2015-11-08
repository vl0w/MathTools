class Dim:
    def __init__(self, height, width=None):
        self.height = height
        if width is None:
            self.width = height
        else:
            self.width = width

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class Matrix:
    def __init__(self, dim):
        self.size = dim
        self.values = []
        for row in range(0, dim.height):
            self.values.append([])
            for column in range(0, dim.width):
                self.values[row].append(0)

    def set(self, row, column, value):
        self.check_element_accessibility(row, column)

        row = self.values[row - 1]
        row[column - 1] = value

    def get(self, row, column):
        self.check_element_accessibility(row, column)

        row = self.values[row - 1]
        return row[column - 1]

    def get_row(self, row):
        # TODO better error handling
        row_matrix = Matrix(Dim(0, 0))
        row_matrix.append_row(self.values[row - 1])
        return row_matrix

    def get_column(self, column_index):
        # TODO better error handling
        # TODO possible to do with transpose?
        column_matrix = Matrix(Dim(self.size.height, 1))
        for row in range(1, self.size.height + 1):
            value = self.get(row, column_index)
            column_matrix.set(row, 1, value)

        return column_matrix

    def append_row(self, row):
        if not self.size.width == 0 and not len(row) == self.size.width:
            raise ValueError("Row must have width of " + str(self.size.width))
        self.values.append(row)
        self.size.height += 1
        self.size.width = len(row)

    def append_column(self, column):
        if not self.size.height == 0 and not column.size.height == self.size.height:
            raise ValueError("Column must have height of " + str(self.size.height))

        # If the matrix is empty, we add 'empty rows' first
        if self.size.height == 0:
            for _ in range(0, column.size.height):
                self.values.append([])
                self.size.height += 1

        for row_index in range(0, self.size.height):
            self.values[row_index].append(column.get(row_index + 1, 1))
        self.size.width += 1

    def on_every_element(self, callback):
        for row in range(1, self.size.height + 1):
            for column in range(1, self.size.width + 1):
                element = self.get(row, column)
                callback(row, column, element)

    def check_element_accessibility(self, row, column):
        if row <= 0 or column <= 0:
            raise ValueError("Row index must be in the range [1;" + str(self.size.height) +
                             "], column index must be in the range [1;" + str(self.size.width) + "]")

        if row > self.size.height or column > self.size.width:
            raise ValueError("Row index must be in the range [1;" + str(self.size.height) +
                             "], column index must be in the range [1;" + str(self.size.width) + "]")

    def join(self, other, callback):
        for r in range(1, self.size.height + 1):
            for c in range(1, self.size.width + 1):
                callback(r, c, self.get(r, c), other.get(r, c))

    def transpose(self):
        transposed_dimension = Dim(self.size.width, self.size.height)
        transposed_matrix = Matrix(transposed_dimension)

        def transpose(row, column, value):
            transposed_matrix.set(column, row, value)

        self.on_every_element(transpose)
        return transposed_matrix

    def exchange_rows(self, source_row_index, target_row_index):
        source_row_copy = self.values[source_row_index - 1]
        self.values[source_row_index - 1] = self.values[target_row_index - 1]
        self.values[target_row_index - 1] = source_row_copy

    def copy(self):
        copied = Matrix(Dim(self.size.height, self.size.width))

        def copy_values(row, column, value):
            copied.set(row, column, value)

        self.on_every_element(copy_values)
        return copied

    def is_square(self):
        return self.size.height == self.size.width

    def upper_triangle(self):
        if not self.is_square():
            raise NotImplementedError("Only square matrices are supported")

        size = self.size.height
        upper_triangle = create_square_matrix(size)

        for r in range(1, size + 1):
            for c in range(1, size + 1):
                if r >= c:
                    continue
                else:
                    upper_triangle.set(r, c, self.get(r, c))

        return upper_triangle

    def lower_triangle(self):
        if not self.is_square():
            raise NotImplementedError("Only square matrices are supported")

        size = self.size.height
        upper_triangle = create_square_matrix(size)

        for r in range(1, size + 1):
            for c in range(1, size + 1):
                if r <= c:
                    continue
                else:
                    upper_triangle.set(r, c, self.get(r, c))

        return upper_triangle

    def diagonal_matrix(self):
        if not self.is_square():
            raise NotImplementedError("Only square matrices are supported")

        size = self.size.height
        diagonal_matrix = create_square_matrix(size)

        for i in range(1, size + 1):
            diagonal_matrix.set(i, i, self.get(i, i))

        return diagonal_matrix

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise ValueError("Addition only allowed with matrix")

        if not self.size == other.size:
            raise ArithmeticError("Matrix dimensions must agree")

        matrix = Matrix(self.size)

        def add(row_index, column_index, value_a, value_b):
            matrix.set(row_index, column_index, value_a + value_b)

        self.join(other, add)

        return matrix

    def __sub__(self, other):
        if not isinstance(other, Matrix):
            raise ValueError("Subtraction only allowed with matrix")

        if not self.size == other.size:
            raise ArithmeticError("Matrix dimensions must agree")

        matrix = Matrix(self.size)

        def subtract(row_index, column_index, value_a, value_b):
            matrix.set(row_index, column_index, value_a - value_b)

        self.join(other, subtract)

        return matrix

    def __rmul__(self, other):
        return self * other

    def __mul__(self, other):
        if isinstance(other, (int, float, complex)):
            matrix = Matrix(self.size)

            def multiply(row_index, column_index, value):
                matrix.set(row_index, column_index, value * other)

            self.on_every_element(multiply)
            return matrix
        elif isinstance(other, Matrix):
            # Check dimensions: Only mxn * nxm allowed
            if not self.size.width == other.size.height:
                raise ArithmeticError("Matrix dimensions must agree (mxn * nxm)")
            if self.size.height == 1 and other.size.width == 1:
                value = 0.0
                for index in range(1, self.size.width + 1):
                    value += self.get(1, index) * other.get(index, 1)
                matrix = Matrix(Dim(1, 1))
                matrix.set(1, 1, value)
                return matrix
            else:
                matrix = Matrix(Dim(self.size.height, other.size.width))
                for row_index in range(1, self.size.height + 1):
                    for column_index in range(1, other.size.width + 1):
                        left_row_matrix = self.get_row(row_index)
                        right_column_matrix = other.get_column(column_index)
                        value_matrix = left_row_matrix * right_column_matrix
                        value = value_matrix.get(1, 1)
                        matrix.set(row_index, column_index, value)
                return matrix
        else:
            raise ValueError("Can only multiply with other matrices and scalars")

    def __str__(self):
        return_value = ""
        for row in range(0, self.size.height):
            for column in range(0, self.size.width):
                return_value += str(self.get(row + 1, column + 1)) + " "
            if not row == self.size.height - 1: # Do not add line break on last line
                return_value += "\n"
        return return_value

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


def create_square_matrix(size):
    return Matrix(Dim(size))


def create_matrix(height, width):
    return Matrix(Dim(height, width))


def create_identity_matrix(size):
    identity = create_square_matrix(size)

    for i in range(1, size + 1):
        identity.set(i, i, 1)

    return identity


def parse_matrix(matrixDefinition):
    import re
    pattern = re.compile("((\d ?)+;?)*")
    if not pattern.match(matrixDefinition):
        raise ValueError("Matrix definition is invalid")

    matrix = create_matrix(0, 0)

    row_definitions = matrixDefinition.split(";")
    for row_definition in row_definitions:
        row = list(map(float, row_definition.split(" ")))
        matrix.append_row(row)

    return matrix
