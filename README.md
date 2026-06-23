# PyMath

Mini bibliothèque Python pour l’algèbre linéaire.

## Features
- Matrices
- Déterminant (n×n)
- Inverse (Gauss-Jordan)
- Résolution de systèmes linéaires

## Example

```python
from pymath import Matrix

A = Matrix([[1,2],[3,4]])

print(A.det())
print(A.inverse())