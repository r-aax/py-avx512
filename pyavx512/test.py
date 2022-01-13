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
    n0, n1, n2 = g.new_node(), g.new_node(), g.new_node()

    # Node 0.
    v0 = ir.load(n0, 'a')
    v1 = ir.load(n0, 'b')
    p0 = ir.cmpge(n0, v0, v1)
    ir.jump(n0, p0, False)
    op3 = n0.LastOper
    ir.jump(n0, p0, True)
    op4 = n0.LastOper

    # Node 1.
    ir.store(n1, ir.add(n1, v0, v1), 'c')

    # Node 2.
    ir.store(n2, ir.sub(n2, v0, v1), 'c')

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
