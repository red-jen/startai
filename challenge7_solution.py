# Challenge 7 Solution: Calcul de distance entre deux points
import math

x1 = float(input("x1 : "))
y1 = float(input("y1 : "))
x2 = float(input("x2 : "))
y2 = float(input("y2 : "))

distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
print("Distance :", distance)