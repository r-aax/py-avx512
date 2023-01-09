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

        self.Counter = 0

    # ----------------------------------------------------------------------------------------------

    def is_start_node(self):
        return self.IEdges == []

    # ----------------------------------------------------------------------------------------------

    def is_stop_node(self):
        return self.OEdges == []

    # ----------------------------------------------------------------------------------------------

    def dump(self):
        """
        Dump node.
        """

        start_str = 'START ' if self.is_start_node() else ''
        stop_str = 'STOP ' if self.is_stop_node() else ''

        # Head.
        start = '{0}{1}CFG Node {2} (cnt = {3}):'.format(start_str, stop_str, self.Id, self.Counter)

        # Opers.
        opers = '\n'.join('{0}'.format(oper) for oper in self.Opers)

        # Foot.
        edges = 'Edges: {0}'.format(', '.join([str(e) for e in self.OEdges]))

        return f'{start}\n{opers}\n{edges}\n'

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
