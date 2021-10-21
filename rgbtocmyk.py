r = int(input("r"))
g = int(input("g"))
b = int(input("b"))

if r == 0 and g == 0 and b == 0 :
    c = m = y = 0
    black = 1
else :
    red = r/255
    green = g/255
    blue = b/255

    max = red
    if green > max :
        max = green

    if blue > max :
        max = blue

    white = max

    c = (white - red) / white
    m = (white - green) / white
    y = (white - blue) / white

    black = 1 - white

    print("c = " + str(c), "m = "  + str(m), "m = " + str(y), "k = " + str(black))