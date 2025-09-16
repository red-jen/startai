
nom = input("entrer votre nom ")
sh = float(input("entrer votre salaire horaire:  "))
ht = float(input("entrer le nombre d'heures travailllees :  "))
if ht > 40 :
    totale = (ht * sh) + ((ht - 40) * sh * 1.5)
else:    
    totale = sh * ht 

print("ur price is ",totale) 

