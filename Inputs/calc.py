#!/usr/bin/python3
class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=None, numCols=None):
        self.matrix = {}
        self.numRows = 0
        self.numCols = 0
        if matrixFilePath:
            self._load_from_file(matrixFilePath)
        else:
            self.numRows = numRows
            self.numCols = numCols

    def _load_from_file(self, matrixFilePath):
        try:
            with open(matrixFilePath, 'r') as file:
                lines = file.readlines()
                self.numRows = int(lines[0].strip().split('=')[1])
                self.numCols = int(lines[1].strip().split('=')[1])
                for line in lines[2:]:
                    if line.strip():
                        row, col, val = map(int, line.strip()[1:-1].split(','))
                        self.matrix[(row, col)] = val
        except Exception as e:
            raise ValueError("Input file has wrong format") from e

    def getElement(self, currRow, currCol):
        return self.matrix.get((currRow, currCol), 0)

    def setElement(self, currRow, currCol, value):
        if value != 0:
            self.matrix[(currRow, currCol)] = value
        elif (currRow, currCol) in self.matrix:
            del self.matrix[(currRow, currCol)]

    def add(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices dimensions do not match for addition")
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        for row in range(self.numRows):
            for col in range(self.numCols):
                sum_value = self.getElement(row, col) + other.getElement(row, col)
                result.setElement(row, col, sum_value)
        return result

    def subtract(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices dimensions do not match for subtraction")
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        for row in range(self.numRows):
            for col in range(self.numCols):
                diff_value = self.getElement(row, col) - other.getElement(row, col)
                result.setElement(row, col, diff_value)
        return result

    def multiply(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Matrices dimensions do not match for multiplication")
        result = SparseMatrix(numRows=self.numRows, numCols=other.numCols)
        for row in range(self.numRows):
            for col in range(other.numCols):
                product_value = 0
                for k in range(self.numCols):
                    product_value += self.getElement(row, k) * other.getElement(k, col)
                result.setElement(row, col, product_value)
        return result

    def __str__(self):
        result = f"rows={self.numRows}\ncols={self.numCols}\n"
        for (row, col), value in sorted(self.matrix.items()):
            result += f"({row}, {col}, {value})\n"
        return result

    def to_file(self, file_path):
        with open(file_path, 'w') as file:
            file.write(str(self))


def main():
    import sys

    if len(sys.argv) != 3:
        print("Usage: python main.py <matrix1_path> <matrix2_path>")
        return

    matrix1_path = sys.argv[1]
    matrix2_path = sys.argv[2]

    matrix1 = SparseMatrix(matrixFilePath=matrix1_path)
    matrix2 = SparseMatrix(matrixFilePath=matrix2_path)

    print("Choose the matrix operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")

    operation = input("Enter the number of the operation (1/2/3): ")

    if operation == '1':
        result = matrix1.add(matrix2)
    elif operation == '2':
        result = matrix1.subtract(matrix2)
    elif operation == '3':
        result = matrix1.multiply(matrix2)
    else:
        print("Unknown operation. Please enter 1, 2, or 3.")
        return

    result.to_file("results.txt")
    print("The result has been written to results.txt")


if __name__ == "__main__":
    main()
