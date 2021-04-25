import numpy as np
import cv2

def encodeNumPyArray(fr, even=False):
    nor = int(float(len(fr) / 2)).to_bytes(2,'big')
    noc = len(fr[0]).to_bytes(2, 'big')

    even_byte = -1
    half_frame = -1

    if(even):
        even_byte = int(1).to_bytes(1, 'big')
        half_frame = fr[1::2]
    else:
        even_byte = int(0).to_bytes(1, 'big')
        half_frame = fr[::2]

    temp = np.array([nor[0],nor[1],noc[0],noc[1], even_byte[0]], np.uint8)

    return np.concatenate((temp, half_frame), axis=None).tobytes()