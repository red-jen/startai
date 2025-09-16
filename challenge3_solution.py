# Challenge 3 Solution: Gestion des erreurs (try/except)
try:
    nom = input("entrer votre nom ")
    sh = float(input("entrer votre salaire horaire: "))
    ht = float(input("entrer le nombre d'heures travaillées: "))
    
    if ht > 40:
        totale = (40 * sh) + ((ht - 40) * sh * 1.5)
    else:
        totale = sh * ht
    
    print("Nom:", nom)
    print("Votre salaire total est:", totale)
except ValueError:
    print("Erreur: Veuillez entrer des nombres valides pour le salaire horaire et les heures travaillées.")
except Exception as e:
    print("Une erreur s'est produite:", str(e))