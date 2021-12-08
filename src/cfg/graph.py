"""
Control flow graph realization.
"""

from cfg.node import Node
from cfg.edge import Edge

# ==================================================================================================


class Graph:

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor.
        """

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
        Adding new node.
        :return: New node.
        """

        node = Node(self)
        node.Id = len(self.Nodes)
        self.Nodes.append(node)

        return node

    # ----------------------------------------------------------------------------------------------

    def add_edge(self, pred, succ):
        """
        Add edge.
        :param pred: Predecessor.
        :param succ: Successor.
        :return: New edge.
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

# ==================================================================================================
