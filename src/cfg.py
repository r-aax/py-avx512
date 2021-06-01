from mask import Mask
from zmm import ZMM
from block import Block


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

    def alloc_block(self):
        """
        Allocate block.

        :return: new block
        """

        block = Block()
        block.Id = len(self.Blocks)
        self.Blocks.append(block)

        return block

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

    # ----------------------------------------------------------------------------------------------

    def emulate(self, i):
        """
        Emulate CFG on position i.

        :param i: index
        """

        # Start emulation with 0-th block.
        block = self.Blocks[0]
        oper_index = 0

        # Infinite loop of emulation.
        while True:

            # If we ca not execute next operation - stop here.
            if oper_index >= len(block.Operations):
                break

            oper = block.Operations[oper_index]

            # Process jump with special case.
            if oper.Type == 'jump':
                if oper.Args[0][i] == oper.Args[1]:
                    block = oper.Res
                    oper_index = 0
                else:
                    oper_index += 1
            else:
                oper.emulate(i)
                oper_index += 1

    # ----------------------------------------------------------------------------------------------

    def emulate_all(self):
        """
        Emulate CFG in all positions.
        """

        # Get width from the result
        # of the first operation of the first block of the CFG.
        n = self.Blocks[0].Operations[0].Res.N

        for i in range(n):
            self.emulate(i)

# ==================================================================================================
