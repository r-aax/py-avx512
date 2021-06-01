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
        self.Operations = []
        self.OpersPerformed = 0

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

    def alloc_argument(self, t):
        """
        Allocate argument of CFG.

        :param t: type
        :return: argument register
        """

        zmm = self.alloc_zmm(t)
        zmm.set_arg()

        return zmm

    # ----------------------------------------------------------------------------------------------

    def alloc_result(self, t):
        """
        Allocate result of CFG.

        :param t: type
        :return: result register
        """

        zmm = self.alloc_zmm(t)
        zmm.set_res()

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
        block.CFG = self
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

    def enter_block(self, b):
        """
        Enter block.

        :param b: block
        :return: block and 0 (index of input operation).
        """

        b.Counter += 1

        return b, 0

    # ----------------------------------------------------------------------------------------------

    def emulate(self, i):
        """
        Emulate CFG on position i.

        :param i: index
        """

        # Start emulation with 0-th block.
        block, oper_index = self.enter_block(self.Blocks[0])

        # Infinite loop of emulation.
        while True:

            # If we ca not execute next operation - stop here.
            if oper_index >= len(block.Operations):
                break

            oper = block.Operations[oper_index]

            # Process jump with special case.
            if oper.Type == 'jump':
                if oper.Args[0] is None:
                    block, oper_index = self.enter_block(oper.Res)
                elif oper.Args[0][i] == oper.Args[1]:
                    block, oper_index = self.enter_block(oper.Res)
                else:
                    oper_index += 1
            else:
                oper.emulate(i)
                self.OpersPerformed += 1
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

    # ----------------------------------------------------------------------------------------------

    def operations_count(self):
        """
        Get operations count.

        :return: operations count
        """

        return len(self.Operations)

    # ----------------------------------------------------------------------------------------------

    def get_arguments(self):
        """
        Get arguments.

        :return: arguments
        """

        return [zmm for zmm in self.ZMMs if zmm.IsA]

    # ----------------------------------------------------------------------------------------------

    def get_results(self):
        """
        Get results.

        :return: results
        """

        return [zmm for zmm in self.ZMMs if zmm.IsR]

    # ----------------------------------------------------------------------------------------------

    def print_arguments_and_results(self):
        """
        Print all arguments and results.
        """

        arguments = self.get_arguments()
        results = self.get_results()

        print('Arguments:')
        for a in arguments:
            print('    {0}'.format(a.str_l()))

        print('Results:')
        for r in results:
            print('    {0}'.format(r.str_l()))

    # ----------------------------------------------------------------------------------------------

    def reset_counters(self):
        """
        Resert operations performed.
        """

        self.OpersPerformed = 0

        for b in self.Blocks:
            b.Counter = 0

# ----------------------------------------------------------------------------------------------

    def print_blocks_counters(self):
        """
        Print all blocks counters.
        """

        print('Blocks counters:')

        hc = float(self.Blocks[0].Counter)

        for b in self.Blocks:
            print('  Block {0} : cnt = {1:5}, prob = {2:8}'.format(b.Id,
                                                                   b.Counter,
                                                                   round(b.Counter / hc, 5)))

# ==================================================================================================
