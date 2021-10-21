from operator import mul

def RGBtoCMYK(r, g, b):
    """
    RGMtoCMYK

    Converts an RGB Palette to a CMYK Palette

    args: (int, int, int)
    ret : (int, int, int, int)
    """
    if r | g | b == 0:
        return (0, 0, 0, 1)

    percentile = lambda x: x / 255

    red   = percentile(r)
    green = percentile(g)
    blue  = percentile(b)
    white = max([red, green, blue])

    build_color = lambda x: round(  \
        mul(                        \
            (white - x) / white,    \
            100                     \
    ))
    
    c = build_color(red)
    m = build_color(green)
    y = build_color(blue)
    k = round((1 - white) * 100)

    return (c, m, y, k)