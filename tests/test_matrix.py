from pymath import Matrix

def test_det():
    A = Matrix([
        [1,2],[3,4]
    ])
    assert A.det() == -2