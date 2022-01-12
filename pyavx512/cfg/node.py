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

    # ----------------------------------------------------------------------------------------------

    def print(self):
        """
        Print node.
        """

        # Head.
        print('CFG Node {0}:'.format(self.Id))

        # Opers.
        for oper in self.Opers:
            print('  {0}'.format(oper))

        # Foot.
        print('Edges: {0}'.format(', '.join([str(e) for e in self.OEdges])))

# ==================================================================================================