from mask import Mask
from zmm import ZMM
from operation import Operation

# ==================================================================================================

if __name__ == '__main__':

    a = ZMM('f')
    a.set_all_elements(1.0)
    b = ZMM('f')
    b.set_all_elements(2.0)
    r = ZMM('f')
    p = Mask(16)
    p[0] = True
    p[3] = True
    p[4] = True

    oper = Operation('add-f', [a, b], r, p, True)
    oper.emulate_all()
    oper.print_s()
    oper.print_l()

# ==================================================================================================
