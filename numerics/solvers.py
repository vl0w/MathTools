from numerics.matrix import *
from numerics.matrix_tools import lu_decomposition


def inv(matrix):
    if not matrix.is_square():
        raise ValueError("Inverse only exists for square matrices")

    size = matrix.size.height

    inverse = create_matrix(0, 0)

    for row_index in range(1, size + 1):
        result_matrix = create_matrix(size, 1)
        result_matrix.set(row_index, 1, 1)

        solution_matrix = gaussian_elimination(matrix, result_matrix)
        inverse.append_column(solution_matrix)

    return inverse


def gaussian_elimination(coefficient_matrix, result_matrix):
    augmented_matrix = coefficient_matrix.copy()
    augmented_matrix.append_column(result_matrix.copy())

    augmented_matrix = lu_decomposition(augmented_matrix).U
    result_column_index = augmented_matrix.size.width;

    solution_matrix = create_matrix(coefficient_matrix.size.height, 1)

    # Backward substitution
    for i in range(0, coefficient_matrix.size.height):
        solution_index = augmented_matrix.size.height - i

        right_side = augmented_matrix.get(solution_index, result_column_index)
        left_side_coefficient = augmented_matrix.get(solution_index, solution_index)

        subtraction = 0
        for n in range(solution_index, coefficient_matrix.size.width):
            subtraction += augmented_matrix.get(solution_index, n + 1) * solution_matrix.get(n + 1, 1)

        solution = (right_side - subtraction) / left_side_coefficient

        solution_matrix.set(solution_index, 1, solution)

    return solution_matrix


def gauss_seidel_iteration(coefficient_matrix, result_matrix):
    iterations = 50  # Amount of iterations

    D = coefficient_matrix.diagonal_matrix()
    L = coefficient_matrix.lower_triangle()
    U = coefficient_matrix.upper_triangle()

    size = coefficient_matrix.size.height
    x = create_matrix(size, 1)

    # Iterative calculation formula:
    # x(k+1) = (-1) * inv(D + L) * U * x(k) + inv(D + L)* result_matrix
    # ==> We calculate non-changing stuff before iteration
    invDL = inv(D + L)
    A = (-1) * invDL * U
    B = invDL * result_matrix

    for i in range(0, iterations):
        x = A * x + B

    return x


def jacobi_iteration(coefficient_matrix, result_matrix):
    iterations = 50  # Amount of iterations

    D = coefficient_matrix.diagonal_matrix()
    L = coefficient_matrix.lower_triangle()
    U = coefficient_matrix.upper_triangle()

    size = coefficient_matrix.size.height
    x = create_matrix(size, 1)

    # Iterative calculation formula:
    # x(k+1) = (-1) * inv(D) * (L + U) * x(k) + inv(D) * result_matrix
    # ==> We calculate non-changing stuff before iteration
    invD = inv(D)
    A = (-1) * invD * (L + U)
    B = invD * result_matrix

    for i in range(0, iterations):
        x = A * x + B

    return x
