n1 = int(input("enter the first num:  "))
n2 = int(input("enter the second num:   "))

produit = n1 * n2 

if produit > 0:
    print("le produit de ", str(n1) +"avec", str(n2) + "est postive :", produit)

elif produit < 0:
    print("le produit de ", str(n1) +"avec", str(n2) + "est neagative :", produit)
else:
    print("le produit de ",str(n1) + "avec", str(n2) +"est null")
