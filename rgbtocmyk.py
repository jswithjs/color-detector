r = int(input("r"))
g = int(input("g"))
b = int(input("b"))

if r == 0 and g == 0 and b == 0 :
    c = m = y = 0
    black = 1
else :
    r = r/255
    g = g/255
    b = b/255

    max = r
    if g > max :
        max = g

    if b > max :
        max = b

    white = max

    c = (white - r) / white
    m = (white - g) / white
    y = (white - b) / white

    black = 1 - white

    print("c = " + str(c), "m = "  + str(m), "m = " + str(y), "k = " + str(black))