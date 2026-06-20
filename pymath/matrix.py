class Matrix:
    def __init__(self, data):

        if len(data) == 0:
            raise ValueError("La matrice ne peut pas être vide.")

        nb_colonnes = len(data[0])

        for ligne in data:
            if len(ligne) != nb_colonnes:
                raise ValueError("Toutes les lignes doivent avoir le même nombre de colonnes.")

        self.data = data
        self.nb_lignes = len(data)
        self.nb_colonnes = nb_colonnes

    def __str__(self):
        texte = ""
        for ligne in self.data:
            texte += str(ligne) + "\n"

        return texte

    def __add__(self, other):

        # 1. vérifier dimensions
        if self.nb_lignes != other.nb_lignes or self.nb_colonnes != other.nb_colonnes:
            raise ValueError("Matrices de tailles différentes")

        # 2. nouvelle matrice résultat
        result = []

        # 3. parcourir lignes
        for i in range(self.nb_lignes):
            ligne = []

            # 4. parcourir colonnes
            for j in range(self.nb_colonnes):
                valeur = self.data[i][j] + other.data[i][j]
                ligne.append(valeur)

            result.append(ligne)
        return Matrix(result)

    def __mul__(self, other):

        # cas scalaire
        if isinstance(other, (int, float)):
            result = []
            for i in range(self.nb_lignes):
                ligne = []
                for j in range(self.nb_colonnes):
                    ligne.append(self.data[i][j] * other)
                result.append(ligne)
            return Matrix(result)

        # cas matrice
        if self.nb_colonnes != other.nb_lignes:
            raise ValueError("Dimensions incompatibles")

        result = []

        for i in range(self.nb_lignes):
            ligne = []
            for j in range(other.nb_colonnes):
                somme = 0
                for k in range(self.nb_colonnes):
                    somme += self.data[i][k] * other.data[k][j]
                ligne.append(somme)
            result.append(ligne)

        return Matrix(result)

    def transpose(self):

        result = []

        for j in range(self.nb_colonnes):  # colonnes deviennent lignes
            ligne = []

            for i in range(self.nb_lignes):  # lignes deviennent colonnes
                ligne.append(self.data[i][j])

            result.append(ligne)

        return Matrix(result)

    @property
    def T(self):
        return self.transpose()

    def __rmul__(self, scalar):

        result = []

        for i in range(self.nb_lignes):
            ligne = []

            for j in range(self.nb_colonnes):
                ligne.append(self.data[i][j] * scalar)

            result.append(ligne)

        return Matrix(result)

    def sub_matrix(self, row, col):

        data = []

        for i in range(self.nb_lignes):
            if i == row:
                continue

            ligne = []

            for j in range(self.nb_colonnes):
                if j == col:
                    continue
                ligne.append(self.data[i][j])

            data.append(ligne)

        return Matrix(data)

    def det(self):

        if self.nb_lignes != self.nb_colonnes:
            raise ValueError("La matrice doit être carrée")

        # cas 1x1
        if self.nb_lignes == 1:
            return self.data[0][0]

        # cas 2x2
        if self.nb_lignes == 2:
            a = self.data[0][0]
            b = self.data[0][1]
            c = self.data[1][0]
            d = self.data[1][1]
            return a * d - b * c

        det_total = 0

        # développement sur la première ligne
        for j in range(self.nb_colonnes):
            signe = (-1) ** j
            element = self.data[0][j]
            sous_matrice = self.sub_matrix(0, j)

            det_total += signe * element * sous_matrice.det()

        return det_total

    @staticmethod
    def identity(n):

        data = []

        for i in range(n):
            ligne = []
            for j in range(n):
                if i == j:
                    ligne.append(1)
                else:
                    ligne.append(0)
            data.append(ligne)

        return Matrix(data)

    def inverse(self):

        if self.nb_lignes != self.nb_colonnes:
            raise ValueError("Matrice non carrée")

        n = self.nb_lignes

        # matrice augmentée [A | I]
        A = [row[:] + identity_row[:] for row, identity_row in zip(self.data, Matrix.identity(n).data)]

        # élimination de Gauss-Jordan
        for i in range(n):

            # pivot partiel
            max_row = i
            for k in range(i + 1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k

            if max_row != i:
                A[i], A[max_row] = A[max_row], A[i]

            pivot = A[i][i]

            if abs(pivot) < 1e-12:
                raise ValueError("Matrice singulière ou instable")

            # normalisation
            for j in range(2 * n):
                A[i][j] /= pivot

            # élimination
            for k in range(n):
                if k != i:
                    facteur = A[k][i]
                    for j in range(2 * n):
                        A[k][j] -= facteur * A[i][j]
        # extraire la partie droite
        inverse_data = []

        for i in range(n):
            inverse_data.append(A[i][n:])

        return Matrix(inverse_data)

    def round_matrix(self, ndigits=10):
        data = []

        for i in range(self.nb_lignes):
            ligne = []
            for j in range(self.nb_colonnes):
                ligne.append(round(self.data[i][j], ndigits))
            data.append(ligne)

        return Matrix(data)

    def solve(self, b):

        if self.nb_lignes != self.nb_colonnes:
            raise ValueError("La matrice doit être carrée")

        n = self.nb_lignes

        # matrice augmentée [A | b]
        A = []
        for i in range(n):
            A.append(self.data[i][:] + [b[i]])

        # élimination de Gauss-Jordan avec pivot partiel
        for i in range(n):

            # pivot partiel
            max_row = i
            for k in range(i + 1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k

            if max_row != i:
                A[i], A[max_row] = A[max_row], A[i]

            pivot = A[i][i]

            if abs(pivot) < 1e-12:
                raise ValueError("Système impossible ou instable")

            # normalisation de la ligne pivot
            for j in range(n + 1):
                A[i][j] /= pivot

            # élimination des autres lignes
            for k in range(n):
                if k != i:
                    facteur = A[k][i]
                    for j in range(n + 1):
                        A[k][j] -= facteur * A[i][j]

        # extraction de la solution
        x = []
        for i in range(n):
            x.append(A[i][n])

        return x


