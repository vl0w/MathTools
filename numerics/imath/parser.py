from numerics.matrix import create_matrix, create_square_matrix


class FileParser:
    def __init__(self, filePath):
        self.filePath = filePath
        self.results = None
        self.coefficients = None

    def parse(self):
        with open(self.filePath) as f:
            file_content = f.readlines()

        # First section: Amount of equations
        self.numberOfEquations = int(file_content[0])

        # Second section: Coefficient matrix
        self.coefficients = create_square_matrix(self.numberOfEquations)
        for row in range(0, self.numberOfEquations):
            splitted_row = file_content[row + 1].split()
            for column in range(0, self.numberOfEquations):
                coefficient = int(splitted_row[column])
                self.coefficients.set(row + 1, column + 1, coefficient)

        # Third section: Result matrix
        self.results = create_matrix(self.numberOfEquations, 1)
        for row in range(0, self.numberOfEquations):
            result = int(file_content[row + 4])
            self.results.set(row + 1, 1, result)
