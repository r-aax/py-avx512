"""
Control flow graph node realization.
"""


# ==================================================================================================


class Node:
    """
    Node class.
    """

    # ----------------------------------------------------------------------------------------------

    def __init__(self, graph):
        """
        Constructor.

        Parameters
        ----------
        graph : cfg.Graph
            Graph.
        """

        self.Graph = graph

        # Identifier.
        self.Id = graph.new_node_id()

        # Input and output edges list.
        self.IEdges = []
        self.OEdges = []

        # Opers.
        self.Opers = []

    # ----------------------------------------------------------------------------------------------

    def dump(self):
        """
        Dump node.
        """

        # Head.
        start = 'CFG Node {0}:'.format(self.Id)

        # Opers.
        opers = '\n'.join('\t{0}'.format(oper) for oper in self.Opers)

        # Foot.
        edges = 'Edges: {0}'.format(', '.join([str(e) for e in self.OEdges]))

        return f'{start}\n{opers}\n{edges}'

    # ----------------------------------------------------------------------------------------------

    def print(self):
        """
        Print node.
        """

        print(self.dump())

    # ----------------------------------------------------------------------------------------------

    @property
    def FirstOper(self):
        """
        Get first oper.

        Returns
        -------
        oper : sem.Oper
            First oper.
        """

        return self.Opers[0]

    # ----------------------------------------------------------------------------------------------

    @property
    def LastOper(self):
        """
        Get last oper.

        Returns
        -------
        oper : sem.Oper
            Last oper.
        """

        return self.Opers[-1]

# ==================================================================================================
