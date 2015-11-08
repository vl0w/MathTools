from numerics.matrix import *


def lu_decomposition(matrix):
    class LU:
        def __init__(self, L, U):
            self.L = L
            self.U = U

    U = permutate_by_first_pivot(matrix)
    L = create_identity_matrix(matrix.size.height)

    for column in range(1, matrix.size.width):
        inv_of_L = create_identity_matrix(matrix.size.height)
        for row in range(1 + column, matrix.size.height + 1):
            l = U.get(row, column) / U.get(column, column)
            inv_of_L.set(row, column, (-1) * l)
            L.set(row, column, l)
        U = inv_of_L * U

    return LU(L, U)


def permutate_by_first_pivot(matrix):
    continue_exchange = True

    while continue_exchange:
        continue_exchange = False
        for row in range(2, matrix.size.height + 1):
            if matrix.get(row, 1) > matrix.get(row - 1, 1):
                matrix.exchange_rows(row, row - 1)
                continue_exchange = True

    return matrix
