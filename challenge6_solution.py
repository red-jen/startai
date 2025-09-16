# Challenge 6 Solution: Inversion de chaîne
word = input("Entrez une chaîne à inverser : ")

# Utilisation d'une boucle while pour inverser la chaîne
i = len(word) - 1
inverse = ""
while i >= 0:
    inverse += word[i]
    i -= 1

print("Chaîne inversée :", inverse)