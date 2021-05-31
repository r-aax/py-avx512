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
        self.Blocks = []

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

    # ----------------------------------------------------------------------------------------------

    def add_block(self, block):
        """
        Add block to CFG.

        :param bl: block
        """

        self.Blocks.append(block)

    # ----------------------------------------------------------------------------------------------

    def add_blocks(self, blocks):
        """
        Add blocks to CFG.

        :param blocks: blocks list
        """

        for block in blocks:
            self.Blocks.append(block)

    # ----------------------------------------------------------------------------------------------

    def print_s(self):
        """
        Print short version of CFG.
        """

        print('CFG')
        print('========== ========== ========== ========== ==========')

        for i, block in enumerate(self.Blocks):
            if i > 0:
                print('---------- ---------- ---------- ---------- ----------')
            block.print_s()

        print('========== ========== ========== ========== ==========')

    # ----------------------------------------------------------------------------------------------

    def print_l(self):
        """
        Print short version of CFG.
        """

        print('CFG')
        print('========== ========== ========== ========== ==========')

        for i, block in enumerate(self.Blocks):
            if i > 0:
                print('---------- ---------- ---------- ---------- ----------')
            block.print_l()

        print('========== ========== ========== ========== ==========')

# ==================================================================================================
