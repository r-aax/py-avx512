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


def case_parser_parse(name, input, result):
    """
    Build case with parser.
    """

    parser = sem.Parser()
    cfg, ir = parser.parse(f'cases/{name}')

    ir.print()
    emu = tools.Emulator(True)
    data = emu.run(ir, input)

    for k, v in result.items():
        for i in range(len(v)):
            isclose(result[k][i], data[k][i], k)


def isclose(expected, actual, k, rel_tol=1e-09, abs_tol=0.1):
    ok = abs(expected - actual) <= max(rel_tol * max(abs(expected), abs(actual)), abs_tol)
    if not ok:
        raise AssertionError(f'Param name {k}: got {actual}, expected {expected}.')


# ==================================================================================================


if __name__ == '__main__':

    ab = {
        'a': [6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0],
        'b': [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    }

    riemann_guessp = {'dl': [1], 'ul': [2], 'pl': [3], 'cl': [4], 'dr': [5], 'ur': [6], 'pr': [7], 'cr': [8]}

    # case_001_build_manual()
    # case_parser_parse('001_if.c',ab, {'c': [6.0, 6.0, 6.0, 0.0, -2.0, -4.0, -6.0]})
    # case_parser_parse('002_if2.c',ab, {'c': [6.0, 6.0, 6.0, 0.0, -2.0, -4.0, -6.0], 'd': [0.0, 5.0, 8.0, 9.0, 0.5, 0.2, 0.0]})
    # case_parser_parse('003_cnst.c',ab, {'c': [6.5, 6.5, 6.5, 9.0, -2.5, -4.5, -6.5]})
    # case_parser_parse('004_cnst_fold.c', ab, {'c': [6.0, 6.0, 6.0, 0.7833333333333332, 6.0, 6.0, 6.0]})
    case_parser_parse('010_riemann_guessp.c', riemann_guessp, {'pm': [-94059.6]})

    # ==================================================================================================
