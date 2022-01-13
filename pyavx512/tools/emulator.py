"""
Emulator realization.
"""

# ==================================================================================================

class Emulator:
    """
    Emulator.
    """

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor.
        """

        pass

    # ----------------------------------------------------------------------------------------------

    def run(self, ir, data):
        """
        Run emulator.

        Parameters
        ----------
        ir : sem.IR
            Intermediate representation.
        data
            Input data.

        Returns
        -------
            Output data.
        """

        cases = len(list(data.values())[0])

        print(f'tools:emulator : run {cases} cases with {data}')

        for i in range(cases):
            # Init runtime values for input parameters.
            for ip in ir.InParams:
                ip.RuntimeVal = data[ip.Id][i]
            self.single_run(ir)

    # ----------------------------------------------------------------------------------------------

    def single_run(self, ir):
        """
        Run with single set of data.

        Parameters
        ----------
        ir : sem.IR
            Intermediate representation.
        """

        print('-- single run --')

        cur_node = ir.CFG.StartNode
        cur_oper_i = 0

        # Emulate while we can do it.
        while True:
            # Check end of emulation.
            if cur_oper_i >= len(cur_node.Opers):
                break

            cur_oper = cur_node.Opers[cur_oper_i]
            print(f'    {cur_node.Id} {cur_oper.Id}')

            # Move to next operation.
            if cur_oper.is_runtime_jump():
                new_node = None
                for e in cur_node.OEdges:
                    if e.Jump == cur_oper:
                        new_node = e.Succ
                        break
                if new_node is None:
                    raise Exception('py-avx512 : jump operation {0} to nowhere'.format(str(cur_oper)))
                cur_node = new_node
                cur_oper_i = 0
            else:
                cur_oper_i += 1

# ==================================================================================================
