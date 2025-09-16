word = input("Entrez  : ")


i = len(word) - 1
inverse = ""
while i >= 0:
    inverse += word[i]
    i -= 1

print("Chaîne inversée :", inverse)
