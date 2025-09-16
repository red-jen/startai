# Challenge 2 Solution: Calcul de salaire avec heures supplémentaires
nom = input("entrer votre nom ")
sh = float(input("entrer votre salaire horaire: "))
ht = float(input("entrer le nombre d'heures travaillées: "))

if ht > 40:
    totale = (40 * sh) + ((ht - 40) * sh * 1.5)
else:
    totale = sh * ht

print("Nom:", nom)
print("Votre salaire total est:", totale)