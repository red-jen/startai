




# ch=input("donner: ")

# def plus_long(ch):
#     p=ch.find(" ")
#     if p==-1:
#         return ch
#     maximum=""
#     mot=""
#     while p!=-1:
#         mot=ch[:p]
#         print(mot)
#         ch=ch[p+1:]
#         print(ch)
#         if len(mot)>len(maximum):
#             maximum=mot
#         p=ch.find(" ")
        
#     return maximum

# print("maximum est: ",plus_long(ch))


# word = input("enter a word: ")

# def howmanytimes(word):
#     repeated = ""
#     for i in range(len(word)):
#         count = 0
#         for j in range(len(word)):
#             if word[i] == word[j]:
#                 count += 1
      
#         if count > 1 and word[i] not in repeated:
#             print(f"Character '{word[i]}' is repeated {count} times.")
#             repeated += word[i]

# howmanytimes(word)


# notes = [12, 4, 14, 11, 18, 13, 7, 10, 5, 9, 15, 8, 14, 16]
# mpx = 0
# for i in range(len(notes)):
#     mpx += notes[i]

# moyenne = mpx / len(notes)

# for j in range(len(notes)):
#     if notes[j] >= moyenne:
#         print( mpx , notes[j])
word = " dibaazbdba zdaibdiab azdidazb dznadb mot"
wort = " odazbazb zdabjazbd azdnbzad zabdjazb mot"



p = word.find(" ")

cas =word[p:]

#  Écrivez du code Python ici
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



   









    




