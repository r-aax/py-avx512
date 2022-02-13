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

    @property
    def StartNode(self):
        """
        Get start node.

        Returns
        -------
        node : cfg.Node
            Start node.
        """

        return self.Nodes[0]

    # ----------------------------------------------------------------------------------------------

    @property
    def StopNode(self):
        """
        Get stop node.

        Returns
        -------
        node : cfg.Node
            Stop node.
        """

        return self.Nodes[-1]

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

    def new_edge(self, pred, succ, jump):
        """
        Add new edge.

        Parameters
        ----------
        pred : Node
            Predecessor node.
        succ : Node
            Successor node.
        jump : Oper
            Jump oper.

        Returns
        -------
        edge : Edge
            New added edge.
        """

        edge = cfg.Edge(pred, succ, jump)
        pred.OEdges.append(edge)
        succ.IEdges.append(edge)
        self.Edges.append(edge)

        return edge

    # ----------------------------------------------------------------------------------------------

    def reset_profile(self):
        for node in self.Nodes:
            node.Counter = 0

        for edge in self.Edges:
            edge.Counter = 0

    # ----------------------------------------------------------------------------------------------

    def print(self):
        """
        Print CFG graph.
        """

        print(self.dump())

    # ----------------------------------------------------------------------------------------------

    def dump(self):
        return '\n'.join(node.dump() for node in self.Nodes)

# ==================================================================================================
