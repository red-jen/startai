# Challenge 2 (Listes) Solution: Mots communs
Ch1 = "Le langage Python est très populaire"
Ch2 = "Python est un langage puissant"

# Découper les chaînes en mots (sans split)
def decouper(chaine):
    mots = []
    mot = ""
    for c in chaine:
        if c == " ":
            if mot != "":
                mots.append(mot)
                mot = ""
        else:
            mot += c
    if mot != "":
        mots.append(mot)
    return mots

mots1 = decouper(Ch1)
mots2 = decouper(Ch2)

# Chercher les mots communs sans set ni intersection
communs = []
for m1 in mots1:
    for m2 in mots2:
        if m1 == m2:
            deja = False
            for c in communs:
                if c == m1:
                    deja = True
            if not deja:
                communs.append(m1)

print(communs)