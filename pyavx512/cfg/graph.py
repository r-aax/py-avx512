"""
Control flow graph realization.
"""

import cfg

# ==================================================================================================


class Graph:
    """
    Control flow graph class.
    """

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor.
        """

        # All nodes.
        self.Nodes = []

        # All edges.
        self.Edges = []

    # ----------------------------------------------------------------------------------------------

    def new_node_id(self):
        """
        Get identifier for new node.

        Returns
        -------
        id : int
            Identifier for new node.
        """

        if not self.Nodes:
            return 0
        else:
            return max([n.Id for n in self.Nodes]) + 1

    # ----------------------------------------------------------------------------------------------

    def new_node(self):
        """
        Add new node.

        Returns
        -------
        node : Node
            Added new node.
        """

        node = cfg.Node(self)
        self.Nodes.append(node)

        return node

    # ----------------------------------------------------------------------------------------------

    def new_edge(self, pred, succ):
        """
        Add new edge.

        Parameters
        ----------
        pred : Node
            Predecessor node.
        succ : Node
            Successor node.

        Returns
        -------
        edge : Edge
            New added edge.
        """

        edge = cfg.Edge(pred, succ)
        pred.OEdges.append(edge)
        succ.IEdges.append(edge)
        self.Edges.append(edge)

        return edge

    # ----------------------------------------------------------------------------------------------

    def new_oper_id(self):
        """
        Get identifier for new operation.

        Returns
        -------
        id : int
            Identifier for new operation.
        """

        if not self.Opers:
            return 0
        else:
            return max([oper.Id for oper in self.Opers]) + 1

    # ----------------------------------------------------------------------------------------------

    def print(self):
        """
        Print CFG graph.
        """

        print('CFG Graph:')

        for node in self.Nodes:
            print('')
            node.print()

# ==================================================================================================
