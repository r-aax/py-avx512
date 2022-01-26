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

    # Semantic.
    ir.set_cur_node(n0)
    v0 = ir.load('a')
    v1 = ir.load('b')
    p0 = ir.cmpge(v0, v1)
    ir.jump(n1, p0, True)
    ir.jump(n2, p0, False)
    #
    ir.set_cur_node(n1)
    ir.store(ir.add(v0, v1), 'c')
    #
    ir.set_cur_node(n2)
    ir.store(ir.sub(v0, v1), 'c')

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


def case_parser_parse(name, result):
    """
    Build case with parser.
    """

    parser = sem.Parser()
    cfg, ir = parser.parse(f'cases/{name}')

    ir.print()
    emu = tools.Emulator(True)
    data = emu.run(ir,
                   {
                       'a': [6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0],
                       'b': [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
                   })

    assert result == data


# ==================================================================================================


if __name__ == '__main__':
    # case_001_build_manual()
    # case_parser_parse('001_if.c', {'c': [6.0, 6.0, 6.0, 0.0, -2.0, -4.0, -6.0]})
    # case_parser_parse('002_if2.c', {'c': [6.0, 6.0, 6.0, 0.0, -2.0, -4.0, -6.0], 'd': [0.0, 5.0, 8.0, 9.0, 0.5, 0.2, 0.0]})
    # case_parser_parse('003_cnst.c', {'c': [6.5, 6.5, 6.5, 9.0, -2.5, -4.5, -6.5]})
    case_parser_parse('004_cnst_fold.c', {'c': [6.5, 6.5, 6.5, 9.0, -2.5, -4.5, -6.5]})

# ==================================================================================================
