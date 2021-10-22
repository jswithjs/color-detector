import numpy as np
np.seterr(divide='ignore', invalid='ignore')

def percentage(i, c):
    print(i, c)
    r  = i
    r /= sum(c)
    r *= 100
    print(r)
    r = round(r)
    r = r.__str__()
    r += '%'
    return r

def rImage(bgr):
    
    bgr = bgr / 255

    K = 1 - np.max(bgr, axis=2)
    C = (1 - bgr[..., 2] - K) / (1 - K)
    M = (1 - bgr[..., 1] - K) / (1 - K)
    Y = (1 - bgr[..., 0] - K) / (1 - K)
    
    C = C[~np.isnan(C)]
    M = M[~np.isnan(M)]
    Y = Y[~np.isnan(Y)]
    K = K[~np.isnan(K)]

    # C = (C * 255).astype(np.uint8)
    # M = (M * 255).astype(np.uint8)
    # Y = (Y * 255).astype(np.uint8)
    # K = (K * 255).astype(np.uint8)

    C = C.flatten()
    M = M.flatten()
    Y = Y.flatten()
    K = K.flatten()

    CMYK = list(map(np.average, [C, M, Y, K]))
    [C, M, Y, K] = CMYK
    ret = {
        'C': percentage(C, CMYK),
        'M': percentage(M, CMYK),
        'Y': percentage(Y, CMYK),
        'K': percentage(K, CMYK)
    }
    return ret