from matexpr import MatrixExpr, ShapeError, ZeroMatrix
from sympy import Add, Basic, sympify
from sympy.rules import (rm_id, unpack, flatten, sort, condition, debug,
        exhaust, do_one, glom)

class MatAdd(MatrixExpr):
    """A Sum of Matrix Expressions

    MatAdd inherits from and operates like SymPy Add

    >>> from sympy import MatAdd, MatrixSymbol
    >>> A = MatrixSymbol('A', 5, 5)
    >>> B = MatrixSymbol('B', 5, 5)
    >>> C = MatrixSymbol('C', 5, 5)
    >>> MatAdd(A, B, C)
    A + B + C
    """
    is_MatAdd = True

    def __new__(cls, *args, **kwargs):
        evaluate = kwargs.get('evaluate', True)
        check    = kwargs.get('check'   , True)

        # TODO: This is a kludge
        # We still use Matrix + 0 in a few places. This removes it
        # In particular see matrix_multiply
        args = [x for x in args if not x == 0]

        obj = Basic.__new__(cls, *args)
        if check:
            validate(*args)
        if evaluate:
            return canonicalize(obj)
        else:
            return obj

    @property
    def shape(self):
        return self.args[0].shape

    def _entry(self, i, j):
        return Add(*[arg._entry(i, j) for arg in self.args])

    def _eval_transpose(self):
        from transpose import Transpose
        return MatAdd(*[Transpose(arg) for arg in self.args])

    def _eval_adjoint(self):
        from adjoint import Adjoint
        return MatAdd(*[Adjoint(arg) for arg in self.args])

    def _eval_trace(self):
        from trace import Trace
        return MatAdd(*[Trace(arg) for arg in self.args])

    def canonicalize(self):
        return canonicalize(self)

def validate(*args):
    if not all(arg.is_Matrix for arg in args):
        raise TypeError("Mix of Matrix and Scalar symbols")
    A = args[0]
    for B in args[1:]:
        if A.shape != B.shape:
            raise ShapeError("Matrices %s and %s are not aligned"%(A,B))

factor_of = lambda arg: arg.as_coeff_mmul()[0]
matrix_of = lambda arg: unpack(arg.as_coeff_mmul()[1])
def combine(cnt, mat):
    from matmul import MatMul
    if cnt == 1:
        return mat
    else:
        return cnt * mat

rules = (rm_id(lambda x: x == 0 or isinstance(x, ZeroMatrix)),
         unpack,
         flatten,
         glom(matrix_of, factor_of, combine),
         sort(str))

canonicalize = exhaust(condition(lambda x: isinstance(x, MatAdd),
                                 do_one(*rules)))
