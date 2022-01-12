"""
Control flow graph edge realization.
"""

# ==================================================================================================


class Edge:
    """
    Edge class.
    """

    # ----------------------------------------------------------------------------------------------

    def __init__(self, pred, succ):
        """
        Constructor.

        Parameters
        ----------
        pred : Node
            Predecessor node.
        succ : Node
            Successor node.
        """

        # Operation.
        # TODO:
        #   Here we need reference to operation.
        self.Oper = None

        # Predecessor node.
        self.Pred = pred

        # Successor node.
        self.Succ = succ

    # ----------------------------------------------------------------------------------------------

    def __str__(self):
        """
        String representation.

        Returns
        -------
        string : str
            String representation.
        """

        return '[{0} -> {1}]'.format(self.Pred.Id, self.Succ.Id)

# ==================================================================================================
