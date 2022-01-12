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
        graph : Graph
            Graph.
        """

        self.Graph = graph

        # Identifier.
        self.Id = None

        # Input and output edges list.
        self.IEdges = []
        self.OEdges = []

        # Operations.
        self.Opers = []

    # ----------------------------------------------------------------------------------------------

    def print(self):
        """
        Print node.
        """

        # Head.
        sf = ''
        if not self.IEdges:
            sf = ' (Start)'
        elif not self.OEdges:
            sf = ' (Stop)'
        print('CFG Node {0}{1}:'.format(self.Id, sf))

        # Opers.
        for oper in self.Opers:
            print('  {0}'.format(oper))

        # Foot.
        print('Edges: {0}'.format(', '.join([str(e) for e in self.OEdges])))

# ==================================================================================================
