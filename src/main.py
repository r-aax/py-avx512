from mask import Mask
from zmm import ZMM

# ==================================================================================================

if __name__ == '__main__':

    m = Mask(16)
    print(m)

    zmmf = ZMM('f')
    print(zmmf)

    zmmf2 = zmmf.copy()
    zmmf2[3] = 2.0
    print(zmmf)
    print(zmmf2)

# ==================================================================================================
