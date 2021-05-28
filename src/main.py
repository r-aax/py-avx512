from mask import Mask
from zmm import ZMM

# ==================================================================================================

if __name__ == '__main__':

    m = Mask(16)
    print(m)

    zmmf = ZMM('f')
    print(zmmf)

    zmmd = ZMM('d')
    print(zmmd)

    zmmi = ZMM('i')
    print(zmmi)

# ==================================================================================================
