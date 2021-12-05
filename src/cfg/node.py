"""
Control flow graph node realization.
"""

# ==================================================================================================


class Node:

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor.
        """

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
        if self.IEdges == []:
            sf = ' (Start)'
        elif self.OEdges == []:
            sf = ' (Stop)'
        print('CFG Node {0}{1}:'.format(self.Id, sf))

        # Opers.
        for oper in self.Opers:
            print('  {0}'.format(oper))

        # Foot.
        print('Edges: {0}'.format(', '.join([str(e) for e in self.OEdges])))

# ==================================================================================================
