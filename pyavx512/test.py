"""
Test file.
"""

import cfg
import du

# ==================================================================================================


def case_001_build_manual():
    """
    Build case_001 inner representation manually.
    """

    g = cfg.Graph()

    # Node 0.
    n0 = g.new_node()
    n0.Opers = []

    # Node 1.
    n1 = g.new_node()
    n1.Opers = [' 1. BEGIN', ' 2. P0 = a > b', ' 3. JUMP P0==T', ' 4. JUMP P0=F', ' 5. END']

    # Node 2.
    n2 = g.new_node()
    n2.Opers = [' 6. BEGIN', ' 7. V0 = a + b', ' 8. R = V0', ' 9. END']

    # Node 3.
    n3 = g.new_node()
    n3.Opers = ['10. BEGIN', '11. V1 = a - b', '12. R = V1', '13. END']

    # Node 4.
    n4 = g.new_node()
    n4.Opers = []

    # Add edges.
    g.add_edge(n0, n1)
    g.add_edge(n1, n2)
    g.add_edge(n1, n3)
    g.add_edge(n2, n4)
    g.add_edge(n3, n4)

    # Print.
    g.print()

# ==================================================================================================


def case_001_parser_parse():
    """
    Build case_001 with parser.
    """

    parser = cfg.Parser()
    parser.parse('cases/001_if.c').print()

# ==================================================================================================


if __name__ == '__main__':
    case_001_build_manual()
    # case_001_parser_parse()

# ==================================================================================================
