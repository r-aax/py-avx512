"""
Test file.
"""

import sem
import tools

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
    ir.new_oper(n0, 'load', [ir.in_param('a')], v0)
    ir.new_oper(n0, 'load', [ir.in_param('b')], v1)
    ir.new_oper(n0, 'cmpge', [v0, v1], p0)
    op3 = ir.new_oper(n0, 'jump', args=[], res=None, predicate=p0, is_invert_predicate=False)
    op4 = ir.new_oper(n0, 'jump', args=[], res=None, predicate=p0, is_invert_predicate=True)

    # Node 1.
    n1 = g.new_node()
    v2 = ir.new_reg()
    ir.new_oper(n1, 'add', [v0, v1], v2),
    ir.new_oper(n1, 'store', [v2, ir.out_param('c')])

    # Node 2.
    n2 = g.new_node()
    v3 = ir.new_reg()
    ir.new_oper(n2, 'sub', [v0, v1], v3),
    ir.new_oper(n2, 'nop', []),
    ir.new_oper(n2, 'nop', []),
    ir.new_oper(n2, 'store', [v3, ir.out_param('c')])

    # Add edges.
    g.new_edge(n0, n1, op3)
    g.new_edge(n0, n2, op4)

    # Print.
    ir.print()

    # Run emulator.
    print('')
    emu = tools.Emulator()
    emu.run(ir,
            {
                'a': [5.0, 4.0, 3.0, 2.0, 1.0, 0.0],
                'b': [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
            })

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
