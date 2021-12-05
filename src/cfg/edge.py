"""
Control flow graph edge realization.
"""

# ==================================================================================================


class Edge:

    # ----------------------------------------------------------------------------------------------

    def __init__(self, pred, succ):
        """
        Constructor.
        :param pred: Predecessor.
        :param succ: Successor.
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
        :return: String.
        """

        return '[{0} -> {1}]'.format(self.Pred.Id, self.Succ.Id)

# ==================================================================================================
