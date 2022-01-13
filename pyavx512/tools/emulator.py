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
                ip.RuntimeVal = data[ip.Val][i]

# ==================================================================================================
