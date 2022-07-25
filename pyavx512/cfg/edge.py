"""
Control flow graph edge realization.
"""

# ==================================================================================================
import math


class Edge:
    """
    Edge class.
    """

    # ----------------------------------------------------------------------------------------------

    def __init__(self, pred, succ, jump):
        """
        Constructor.

        Parameters
        ----------
        pred : Node
            Predecessor node.
        succ : Node
            Successor node.
        jump : Oper
            Operation of jump.
        """

        # Predecessor node.
        self.Pred = pred

        # Successor node.
        self.Succ = succ

        # Jump oper.
        self.Jump = jump

        self.Counter = 0

    # ----------------------------------------------------------------------------------------------

    def __str__(self):
        """
        String representation.

        Returns
        -------
        string : str
            String representation.
        """

        return '[{0}. {1} -> {2}, cnt = {3}, prob = {4}]'.format(self.Jump.Id, self.Pred.Id, self.Succ.Id, self.Counter,
                                                                 self.probability)

    # ----------------------------------------------------------------------------------------------
    @property
    def probability(self):
        """
        Get probability.

        Returns
        -------
        probability : float
            Probability of this edge.
        """

        return round(self.Counter / self.Pred.Counter, 2) if self.Pred.Counter != 0 else math.nan

# ==================================================================================================
