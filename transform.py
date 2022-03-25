import numpy as np


class Identity:

    @staticmethod
    def transform(matrix_2d):
        return matrix_2d

    @staticmethod
    def reverse(matrix_2d):
        return matrix_2d


class Flip:
    def __init__(self, op):
        self.op = op

    def transform(self, matrix_2d):
        return self.op(matrix_2d)

    def reverse(self, transformed_matrix_2d):
        return self.transform(transformed_matrix_2d)


class Rotate90:
    def __init__(self, rotations_count):
        self.op = np.rot90
        self.rotations_count = rotations_count

    def transform(self, matrix_2d):
        return self.op(matrix_2d, self.rotations_count)

    def reverse(self, transformed_matrix_2d):
        return self.op(transformed_matrix_2d, -self.rotations_count)


class Transform:
    def __init__(self, operations):
        self.operations = operations

    def transform(self, matrix_2d):
        for op in self.operations:
            matrix_2d = op.transform(matrix_2d)
        return matrix_2d

    def reverse(self, transformed_matrix_2d):
        for op in reverse(self.operations):
            transformed_matrix_2d = op.transform(transformed_matrix_2d)
        return transformed_matrix_2d


def reverse(items):
    return items[::-1]
