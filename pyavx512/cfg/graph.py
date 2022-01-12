"""
Control flow graph realization.
"""

from cfg.node import Node
from cfg.edge import Edge

# ==================================================================================================


class Graph:
    """
    Graph class.
    """

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor.
        """

        # Next oper id.
        self._NextOperId = 0

        # All nodes.
        self.Nodes = []

        # Start and stop nodes.
        self.Start = None
        self.Stop = None

        # All edges.
        self.Edges = []

    # ----------------------------------------------------------------------------------------------

    def new_node(self):
        """
        Add new node.

        Returns
        -------
        node : Node
            Added new node.
        """

        node = Node(self)
        node.Id = len(self.Nodes)
        self.Nodes.append(node)

        return node

    # ----------------------------------------------------------------------------------------------

    def add_edge(self, pred, succ):
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

        edge = Edge(pred, succ)
        pred.OEdges.append(edge)
        succ.IEdges.append(edge)
        self.Edges.append(edge)

        return edge

    # ----------------------------------------------------------------------------------------------

    def print(self):
        """
        Print CFG graph.
        """

        print('CFG Graph:')

        for node in self.Nodes:
            print('')
            node.print()

    # ----------------------------------------------------------------------------------------------

    def next_oper_id(self):
        """
        Next operation identifier.

        Returns
        -------
        oper_id : int
            Next operation identifier.
        """

        res = self._NextOperId

        self._NextOperId += 1

        return res

# ==================================================================================================
