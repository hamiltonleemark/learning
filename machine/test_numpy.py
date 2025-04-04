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


