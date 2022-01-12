"""
Test file.
"""

import sem

# ==================================================================================================


def case_001_build_manual():
    """
    Build case_001 inner representation manually.
    """

    ir = sem.IR()
    g = ir.CFG
    ir.set_in_out_params(['a', 'b'], ['c'])

    # Node 0.
    n0 = g.new_node()
    n0.Opers = [' 1. load a -> v0', ' 2. load b -> v1', ' 3. p0 = v0 > v1', ' 4. jump p0', ' 5. jump ~p0']

    # Node 1.
    n1 = g.new_node()
    n1.Opers = [' 6. v2 = v0 + v1', ' 7. store v2 -> c']

    # Node 2.
    n2 = g.new_node()
    n2.Opers = ['8. v3 = v0 - v1', '9. store v3 -> c']

    # Add edges.
    g.new_edge(n0, n1)
    g.new_edge(n0, n2)

    # Print.
    ir.print()

# ==================================================================================================


def case_001_parser_parse():
    """
    Build case_001 with parser.
    """

    parser = sem.Parser()
    parser.parse('cases/001_if.c').print()

# ==================================================================================================


if __name__ == '__main__':
    case_001_build_manual()
    # case_001_parser_parse()

# ==================================================================================================
