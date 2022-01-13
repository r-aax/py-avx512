"""
Control flow graph edge realization.
"""

# ==================================================================================================


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

    # ----------------------------------------------------------------------------------------------

    def __str__(self):
        """
        String representation.

        Returns
        -------
        string : str
            String representation.
        """

        return '[{0}. {1} -> {2}]'.format(self.Jump.Id, self.Pred.Id, self.Succ.Id)

# ==================================================================================================
