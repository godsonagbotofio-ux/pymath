from pymath import Matrix


# -------- INPUT MATRICE --------
def input_matrix():
    n = int(input("Nombre de lignes (max 5) : "))
    m = int(input("Nombre de colonnes (max 5) : "))

    if n > 5 or m > 5:
        print("Erreur : taille maximale 5x5")
        return None

    data = []

    print("Entrer les valeurs ligne par ligne :")

    for i in range(n):
        while True:
            ligne = list(map(float, input(f"Ligne {i+1} : ").split()))
            if len(ligne) != m:
                print("Erreur : mauvais nombre de colonnes")
            else:
                break
        data.append(ligne)

    return Matrix(data)


# -------- MENU --------
def menu():
    print("\n===== PYMATH MENU =====")
    print("1. Afficher matrice")
    print("2. Déterminant")
    print("3. Inverse")
    print("4. Résoudre Ax = b")
    print("0. Quitter")


# -------- MAIN --------
def main():

    A = input_matrix()
    if A is None:
        return

    while True:
        menu()
        choix = input("Choix : ")

        if choix == "1":
            print("\nMatrice A :")
            print(A)

        elif choix == "2":
            try:
                print("Déterminant :", A.det())
            except Exception as e:
                print("Erreur :", e)

        elif choix == "3":
            try:
                print("Inverse :")
                print(A.inverse())
            except Exception as e:
                print("Erreur :", e)

        elif choix == "4":
            try:
                b = list(map(float, input("Entrer b (séparé par espace) : ").split()))

                if len(b) != A.nb_lignes:
                    print("Erreur : taille de b incorrecte")
                else:
                    print("Solution :", A.solve(b))

            except Exception as e:
                print("Erreur :", e)

        elif choix == "0":
            print("Fin du programme")
            break

        else:
            print("Choix invalide")


if __name__ == "__main__":
    main()