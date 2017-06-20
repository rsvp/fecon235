#  Python Module for import                           Date : 2017-06-19
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  yi_matrix.py : Linear algebra module

          Usage:  To easily invert a matrix, use invert() which includes
                  testing for ill-conditioned matrix and fallback to
                  computing the Moore-Penrose pseudo-inverse.

    !!=>  IRONY:  For numpy work, we want to DISCOURAGE the use of np.matrix,
                  which is a subclass of np.ndarray, since their
                  interoperations may produce unexpected results.

                  - The np.matrix subclass is confined to 2-D matrices.
                  - Sticking with array constructs:
                      Operator "*" means element-wise multiplication.
                      For matrix multiplication, using .dot() is best,
                      since operator "@" originates from Python 3.5.
                  - For our arguments, "mat" is mathematically a matrix,
                      but not necessarily designed for subclass np.matrix.
                  - We explicitly avoid np.matrix.I to calculate inverse.
                  - We will assume matrices are of type np.ndarray.

          Tests:  see tests/test_matrix.py, esp. for output examples.

REFERENCES
- Numpy, https://docs.scipy.org/doc/numpy-dev/user/quickstart.html
- Gilbert Strang, 1980, Linear Algebra and Its Applications, 2nd ed. 

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2017-06-19  Add cov2cor().
2017-06-17  First version to numerically understand numpy inverse methods.
'''

from __future__ import absolute_import, print_function, division
import numpy as np
from . import yi_0sys as system


RCOND = 1e-15
#       Cutoff for small singular values.


def is_singular( mat ):
    '''Just test whether matrix is singular (thus not invertible).
       Mathematically, iff det(mat)==0 : NOT recommended numerically.
       If the condition number is very large, then the matrix is said to 
       be "ill-conditioned." Practically such a matrix is almost singular,
       and the computation of its inverse, or solution of a linear system
       of equations is prone to large numerical errors.
       A matrix that is not invertible has condition number equal to 
       infinity mathematically, but here for numerical purposes,
       "ill-conditioned" shall mean condition number exceeds 1/epsilon.
    '''
    #  Ref: https://en.wikipedia.org/wiki/Condition_number
    #  We shall use epsilon for np.float64 data type
    #  since Python’s floating-point numbers are usually 64-bit.
        #  >>> np.finfo(np.float32).eps
        #  1.1920929e-07
        #  >>> sys.float_info.epsilon
        #  2.220446049250313e-16
        #  >>> np.finfo(np.float64).eps
        #  2.2204460492503131e-16
        #  >>> 1/np.finfo(np.float64).eps
        #  4503599627370496.0
    if np.linalg.cond(mat) < 1/ np.finfo(np.float64).eps:
        #       ^2-norm, computed directly using the SVD.
        return False
    else:
        #  Intentionally, no error handling here.
        return True


def invert_caution( mat ):
    '''Compute the multiplicative inverse of a matrix.
       Numerically np.linalg.inv() is generally NOT suitable,
       especially if the matrix is ill-conditioned,
       but it executes faster than invert_pseudo():
          np.linalg.inv() calls numpy.linalg.solve(mat, I)
          where I is identity and uses LAPACK LU FACTORIZATION. 
    '''
    #  Curiously np.linalg.inv() does not test this beforehand:
    if is_singular(mat):
        system.die("invert_caution(): matrix is SINGULAR.")
    else:
        #         LinAlgError if mat is not square.
        return np.linalg.inv( mat )


def invert_pseudo( mat, rcond=RCOND ):
    '''Compute the pseudo-inverse of a matrix.
       If a matrix is invertible, its pseudo-inverse will be its inverse.
       Moore-Penrose algorithm here uses SINGULAR-VALUE DECOMPOSITION (SVD).
    '''
    #  Ref: https://en.wikipedia.org/wiki/Moore–Penrose_pseudoinverse
    #  Mathematically, pseudo-inverse (a.k.a. generalized inverse) is defined 
    #  and unique for all matrices whose entries are real or complex numbers.
    #         LinAlgError if SVD computation does not converge.
    return np.linalg.pinv( mat, rcond )


def invert( mat, rcond=RCOND ):
    '''Compute the inverse, or pseudo-inverse as fallback, of a matrix.'''
    try:
        #  Faster version first, with is_singular() test...
        return invert_caution( mat )
    except:
        #  ... so mat is probably singular:
        system.warn("ILL-CONDITION: invert() may output pseudo-nonsense.")
        #  How did we get here? The problem is most likely collinearity.
        return invert_pseudo( mat, rcond )


def cov2cor( cov, n=6 ):
    '''Covariance array to correlation array, n-decimal places.
       Outputs "Pearson product-moment CORRELATION COEFFICIENTS."
    '''
    #  https://en.wikipedia.org/wiki/Covariance_matrix
    darr = np.diagonal( cov )
    #        ^get diagonal elements of cov into a pure array.
    #         Numpy docs says darr is not writeable, OK.
    D = np.diag( 1.0/np.sqrt(darr) ) 
    #     ^creates diagonal square "matrix" but not of subclass np.matrix.
    cor = D.dot(cov).dot(D)
    return np.round( cor, n )


if __name__ == "__main__":
     system.endmodule()
