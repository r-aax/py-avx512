from mask import Mask
from zmm import ZMM
from operation import Operation

# ==================================================================================================

if __name__ == '__main__':

    a = ZMM('f')
    b = ZMM('f')
    r = ZMM('f')
    p = Mask(16)

    oper = Operation('add-f', [a, b], r, p, True)
    oper.print_s()
    oper.print_l()

# ==================================================================================================
