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
    v0 = ir.new_reg()
    v1 = ir.new_reg()
    p0 = ir.new_predicate()
    n0.Opers = \
    [
        ir.new_oper('load', [ir.in_param('a')], v0),
        ir.new_oper('load', [ir.in_param('b')], v1),
        ir.new_oper('cmpge', [v0, v1], p0),
        ir.new_oper('jump', args=[], res=None, predicate=p0, is_invert_predicate=True),
        ir.new_oper('jump', args=[], res=None, predicate=p0, is_invert_predicate=False)
    ]

    # Node 1.
    n1 = g.new_node()
    v2 = ir.new_reg()
    n1.Opers = \
    [
        ir.new_oper('add', [v0, v1], v2),
        ir.new_oper('store', [v2, ir.out_param('c')])
    ]

    # Node 2.
    n2 = g.new_node()
    v3 = ir.new_reg()
    n2.Opers = \
    [
        ir.new_oper('sub', [v0, v1], v3),
        ir.new_oper('nop', []),
        ir.new_oper('nop', []),
        ir.new_oper('store', [v3, ir.out_param('c')])
    ]

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
