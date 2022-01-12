"""
Intermediate representation.
"""

import cfg

# ==================================================================================================


class IR:
    """
    Intermediate representation.
    """

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor.
        """

        # CFG
        self.CFG = cfg.Graph()

        # In params.
        self.InParams = []

        # Out params.
        self.OutParams = []

        # Virtual registers.
        self.VRegs = []

        # Predicates.
        self.Predicates = []

        # Constants.
        self.Constants = []

        # Operations list.
        self.Opers = []

    # ----------------------------------------------------------------------------------------------

    def set_in_out_params(self, in_params, out_params):
        """
        Set input and output parameters.

        Parameters
        ----------
        in_params : list
            List of input parameters.
        out_params : list
            List of output parameters.
        """

        self.InParams = in_params
        self.OutParams = out_params

    # ----------------------------------------------------------------------------------------------

    def new_vreg_num(self):
        """
        Get number for new virtual register.

        Returns
        -------
        id : int
            Identifier for new virtual register.
        """

        if not self.VRegs:
            return 0
        else:
            return max([vreg.Num for vreg in self.VRegs]) + 1

    # ----------------------------------------------------------------------------------------------

    def new_predicate_num(self):
        """
        Get number for new virtual register.

        Returns
        -------
        id : int
            Identifier for new virtual register.
        """

        if not self.VRegs:
            return 0
        else:
            return max([vreg.Num for vreg in self.VRegs]) + 1

    # ----------------------------------------------------------------------------------------------

    def new_oper_id(self):
        """
        Get identifier for new operation.

        Returns
        -------
        id : int
            Identifier for new operation.
        """

        if not self.Opers:
            return 0
        else:
            return max([oper.Id for oper in self.Opers]) + 1

    # ----------------------------------------------------------------------------------------------

    def print(self):
        """
        Print.
        """

        print('IR:')
        print(f'  in_params = {self.InParams}, out_params = {self.OutParams}')

        self.CFG.print()

# ==================================================================================================
