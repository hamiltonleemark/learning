"""
Learning about numpy.
"""
import numpy
from scipy.sparse import csr_matrix

def test_numpy():
    """ Test numpy. """
    vector = numpy.array([[1],[2],[3]])
    assert vector.any()
    vector = numpy.array([[1, 2],
                          [1, 2],
                          [1, 3]])
    assert vector.any()


def test_sparse():
    """ Test sparse matrix creation. """

    # Create a sparse matrix

    sparse_matrix = csr_matrix([[0, 0, 3], [4, 0, 0], [0, 5, 0]])

    # Check if the sparse matrix is created correctly
    assert sparse_matrix.shape == (3, 3)
    assert sparse_matrix.nnz == 3  # Number of non-zero elements
    assert sparse_matrix[0, 2] == 3
    assert sparse_matrix[1, 0] == 4
    assert sparse_matrix[2, 1] == 5


def test_apply_function():
    """ Testing apply. """

    sparse_matrix = numpy.array([[0, 0, 3], [4, 0, 0], [0, 5, 0]])

    assert sparse_matrix[0, 0] == 0
    assert sparse_matrix[0, 1] == 0
    assert sparse_matrix[0, 2] == 3


    vector_add_1 = numpy.vectorize(lambda item: item + 1)
    new_matrix = vector_add_1(sparse_matrix)

    assert new_matrix[0, 0] == 1
    assert new_matrix[1, 0] == 5

    assert vector_add_1


def test_transpose():
    """ Testing transpose. """

    # pylint: disable=pointless-statement

    matrix = numpy.array([[1, 2, 3],
                          [4, 5, 6],
                          [7, 8, 9]])

    # ignore this
    transpose = matrix.T
    assert transpose[0, 0] == 1
    assert transpose[1, 0] == 2


def test_rank():
    """ Testing rank. """

    matrix = numpy.array([[1, 1, 1],
                          [1, 1, 10],
                          [1, 1, 15]])

    assert numpy.linalg.matrix_rank(matrix) == 2

    ##
    # [[1, 1, 1],
    #  [1, 1, 10],
    #  [1, 1, 15]]
    #
    # -R1 + R2 ->
    # -R1 + R3 ->
    #
    # [[1, 1, 1],
    #  [0, 0, 9],
    #  [0, 0, 14]]
    #
    # [[1, 1, 1],
    #  [0, 0, 9],
    #  [0, 0, 0]]
    ##

    matrix = numpy.array([[1, 2, 3],
                          [2, 4, 6],
                          [-1, -2, -3]])

    rank = numpy.linalg.matrix_rank(matrix)
    assert int(rank) == 1

    matrix = numpy.array([[1, 0, 0],
                          [0, 1, 0],
                          [0, 0, 1]])

    rank = numpy.linalg.matrix_rank(matrix)
    assert int(rank) == 3
