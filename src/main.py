from mask import Mask
from zmm import ZMM
from operation import Operation
from block import Block
from cfg import CFG

# ==================================================================================================

if __name__ == '__main__':

    cfg = CFG()
    bl = Block()

    # Create semantic.
    a = cfg.alloc_zmm('f')
    b = cfg.alloc_zmm('f')
    c = cfg.alloc_zmm('f')
    add_oper = Operation('add-f', [a, b], c)
    bl.add_operation(add_oper)
    d = cfg.alloc_zmm('f')
    e = cfg.alloc_zmm('f')
    mul_oper = Operation('mul-f', [c, d], e)
    bl.add_operation(mul_oper)

    # Values.
    a.set_elements([1.0, 2.0, 3.0])
    b.set_elements([2.0, 3.0, 4.0])
    d.set_elements([3.0, 4.0, 5.0])
    bl.emulate_all()

    bl.print_s()
    bl.print_l()

# ==================================================================================================
