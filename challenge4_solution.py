# Challenge 4 Solution: Déterminer le signe d'un produit
n1 = float(input("Entrez le premier nombre : "))
n2 = float(input("Entrez le deuxième nombre : "))

produit = n1 * n2

if produit > 0:
    print("Le produit est positif.")
elif produit < 0:
    print("Le produit est négatif.")
else:
    print("Le produit est nul.")