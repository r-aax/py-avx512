"""
Test file.
"""
import os

import sem
import tools


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


# ==================================================================================================

def isclose(expected, actual, k, rel_tol=1e-09, abs_tol=0.1):
    ok = abs(expected - actual) <= max(rel_tol * max(abs(expected), abs(actual)), abs_tol)
    if not ok:
        raise AssertionError(f'Param name {k}: got {actual}, expected {expected}.')


# ==================================================================================================

def case_parser_dump():
    input_path = 'cases'
    output_path = 'out'

    parser = sem.Parser()

    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    for entry in os.scandir(input_path):
        if not entry.name.endswith('.c'):
            continue

        f = open(entry.path, "r")
        code = f.read()
        f.close()

        try:
            cfg, ir = parser.parse(entry.path)
            ir_dump = ir.dump()
        except Exception as e:
            ir_dump = f'Err: {e}'

        content = f'{code}\n{ir_dump}'
        f = open(f'{output_path}/{entry.name}.txt', "w")
        f.write(content)
        f.close()


# ==================================================================================================


if __name__ == '__main__':
    # ab = {
    #     'a': [6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0],
    #     'b': [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    # }
    #
    # riemann_guessp = {'dl': [1], 'ul': [2], 'pl': [3], 'cl': [4], 'dr': [5], 'ur': [6], 'pr': [7], 'cr': [8]}
    # riemann_prefun = {'p': [1], 'dk': [2], 'pk': [3], 'ck': [4]}
    # riemann_sample = {'dl': [1], 'ul': [2], 'vl': [3], 'wl': [4], 'pl': [5], 'cl': [6], 'dr': [7], 'ur': [8], 'vr': [9],
    #                   'wr': [10], 'pr': [11], 'cr': [12], 'pm': [13], 'um': [14]}

    # case_parser_parse('001_if.c',ab, {'c': [6.0, 6.0, 6.0, 0.0, -2.0, -4.0, -6.0]})
    # case_parser_parse('002_if2.c',ab, {'c': [6.0, 6.0, 6.0, 0.0, -2.0, -4.0, -6.0], 'd': [0.0, 5.0, 8.0, 9.0, 0.5, 0.2, 0.0]})
    # case_parser_parse('003_cnst.c',ab, {'c': [6.5, 6.5, 6.5, 9.0, -2.5, -4.5, -6.5]})
    # case_parser_parse('004_cnst_fold.c', ab, {'c': [6.0, 6.0, 6.0, 0.7833333333333332, 6.0, 6.0, 6.0]})
    # case_parser_parse('008_pow_ternary.c', ab, {'c': [1.0, 5.0, 16.0, 27.0, 16.0, 5.0, 1.0]})
    # case_parser_parse('009_pow_pow_ternary.c', ab, {'c': [1.0, 3125.0, 1.8446744073709552e+19, 4.434264882430378e+38, 1.8446744073709552e+19, 3125.0, 1.0]})
    # case_parser_parse('010_riemann_guessp.c', riemann_guessp, {'pm': [-94059.6]})
    # case_parser_parse('011_riemann_prefun.c', riemann_prefun, {'f': [-10.666666], 'fd': [1.125]})
    # case_parser_parse('013_riemann_sample.c', riemann_sample,
    #                   {'d': [0.5180722891566264], 'u': [14], 'v': [3], 'w': [4], 'p': [13]})

    case_parser_dump()

    # ==================================================================================================
