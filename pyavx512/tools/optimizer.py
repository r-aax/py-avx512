"""
Optimizer realization.
"""

import sem

# ==================================================================================================


class Optimizer:
    """
    Optimizer.
    """

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor.
        """

        self.CurPhaseNumber = 0

    # ----------------------------------------------------------------------------------------------

    def set_cur_phase_number(self, cur_phase_number):
        """
        Set currect phase number.

        Parameters
        ----------
        cur_phase_number
            Phase number.
        """

        self.CurPhaseNumber = cur_phase_number

    # ----------------------------------------------------------------------------------------------

    def optimize(self, ir, optimization_name):
        """
        Process of optimization.

        Parameters
        ----------
        ir
            Intermediate representation.
        optimization_name
            Name of optimization phase.
        """

        self.CurPhaseNumber += 1

# ==================================================================================================
