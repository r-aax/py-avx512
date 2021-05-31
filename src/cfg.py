from mask import Mask
from zmm import ZMM


# ==================================================================================================

class CFG:

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Create CFG - control flow graph.
        """

        self.ZMMs = []
        self.Masks = []

    # ----------------------------------------------------------------------------------------------

    def alloc_zmm(self, t):
        """
        Allocate virtual register.

        :param t: type
        :return: virtual register
        """

        zmm = ZMM(t)
        zmm.Id = len(self.ZMMs)
        self.ZMMs.append(zmm)

        return zmm

    # ----------------------------------------------------------------------------------------------

    def alloc_mask(self, n=16):
        """
        Allocate mask.

        :param n: count of elements
        :return: mask
        """

        mask = Mask()
        mask.Id = len(self.Masks)
        self.Masks.append(mask)

        return mask

# ==================================================================================================
