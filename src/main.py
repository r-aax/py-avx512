from mask import Mask
from zmm import ZMM
from operation import Operation
from block import Block
from cfg import CFG

# --------------------------------------------------------------------------------------------------


def sample_guessp_cfg():
    """
    CFG for guessp function of riemann solver.
    :return: CFG
    """

    # Constants.
    gama = 1.4
    g1 = (gama - 1.0) / (2.0 * gama)
    g2 = (gama + 1.0) / (2.0 * gama)
    g3 = (2.0 * gama) / (gama - 1.0)
    g4 = 2.0 / (gama - 1.0)
    g5 = 2.0 / (gama + 1.0)
    g6 = (gama - 1.0) / (gama + 1.0)
    g7 = (gama - 1.0) / 2.0
    g8 = gama - 1.0

    cfg = CFG()

    # First block, before jumps.
    block0 = cfg.alloc_block()
    quser = cfg.alloc_zmm('f')
    block0.add_operation(Operation('set', [2.0], quser))

    return cfg


# ==================================================================================================

if __name__ == '__main__':

    cfg = sample_guessp_cfg()

    # Emulate.
    cfg.emulate_all()

    # Print.
    cfg.print_s()
    cfg.print_l()

# ==================================================================================================
