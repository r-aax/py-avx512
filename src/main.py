from mask import Mask
from zmm import ZMM
from operation import Operation
from block import Block
from cfg import CFG

# ==================================================================================================

if __name__ == '__main__':

    cfg = CFG()
    bl_cond = cfg.alloc_block()
    bl_add = cfg.alloc_block()
    bl_mul = cfg.alloc_block()

    # Registers.
    a = cfg.alloc_zmm('f')
    b = cfg.alloc_zmm('f')
    c = cfg.alloc_zmm('f')
    m = cfg.alloc_mask()

    # Semantic.
    cmp_oper = Operation('cmpgt-f', [a, b], m)
    bl_cond.add_operation(cmp_oper)
    add_oper = Operation('add-f', [a, b], c)
    bl_add.add_operation(add_oper)
    mul_oper = Operation('mul-f', [a, b], c)
    bl_mul.add_operation(mul_oper)

    # Values.
    a.set_elements([1.0, 2.0, 3.0])
    b.set_elements([2.0, 3.0, 4.0])

    cfg.print_s()
    cfg.print_l()

# ==================================================================================================
