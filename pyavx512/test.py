"""
Test file.
"""

import cfg

# ==================================================================================================


def case_001_build_manual():
    """
    Build case_001 inner representation manually.
    """

    g = cfg.Graph()

    # Node 0.
    n0 = g.new_node()
    n0.Opers = [' 2. load a -> v0', ' 3. load b -> v1', ' 4. p0 = v0 > v1', ' 5. jump p0', ' 6. jump ~p0']

    # Node 1.
    n1 = g.new_node()
    n1.Opers = [' 9. v2 = v0 + v1', ' 8. store v2 -> c']

    # Node 2.
    n2 = g.new_node()
    n2.Opers = ['11. v3 = v0 - v1', '12. store v3 -> c']

    # Add edges.
    g.add_edge(n0, n1)
    g.add_edge(n0, n2)

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
