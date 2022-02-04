"""
Test file.
"""

import numpy as np
import os
import sem
import tools

# ==================================================================================================


def is_close(expected, actual, k, rel_tol=1e-09, abs_tol=0.1):
    """
    Check if expected and actual results are close.

    Parameters
    ----------
    expected
        Expected result.
    actual
        Actual result.
    k
        Parameter name.
    rel_tol
        Relative accuracy.
    abs_tol
        Absolute accuracy.

    Returns
    -------
        True, if expected and actual results are close,
        False, otherwise.
    """

    ok = abs(expected - actual) <= max(rel_tol * max(abs(expected), abs(actual)), abs_tol)

    if not ok:
        raise AssertionError(f'Param name {k}: got {actual}, expected {expected}.')

# ==================================================================================================


def run_case(name, input, result):
    """
    Run case with results check.

    Parameters
    ----------
    name
        Case name.
    input
        Input data.
    result
        Correct results.
    """

    parser = sem.Parser()
    cfg, ir = parser.parse(f'cases/{name}')

    ir.print()
    emu = tools.Emulator(True)
    data = emu.run(ir, input)

    for k, v in result.items():
        for i in range(len(v)):
            is_close(result[k][i], data[k][i], k)

# ==================================================================================================


def dump_all_cases(names=None):
    """
    Dump all cases from folder "cases".

    Parameters
    ----------
    names
        Names of cases.
    """

    input_path = 'cases'
    output_path = 'out'

    parser_orig = sem.Parser()
    parser_opt = sem.Parser()
    opt = tools.Optimizer()
    emu = tools.Emulator()

    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    for entry in os.scandir(input_path):
        if not names is None:
            if not entry.name.split('.')[0] in names:
                continue
        if not entry.name.endswith('.c'):
            continue

        f = open(entry.path, "r")
        code = f.read()
        f.close()

        try:
            cfg_orig, ir_orig = parser_orig.parse(entry.path)
            cfg_opt, ir_opt = parser_opt.parse(entry.path)
            ir_orig_dump = ir_orig.dump()
            opt.optimize(ir_opt)
            ir_opt_dump = ir_opt.dump()
        except Exception as e:
            ir_dump = f'Err: {e}'

        # Run original and optimized IR.
        input_data = {}
        for in_param in ir_orig.InParams:
            input_data[in_param.Id] = np.random.uniform(-100.0, 100.0, 16)
        res_orig = emu.run(ir_orig, input_data)
        res_opt = emu.run(ir_opt, input_data)

        f = open(f'{output_path}/{entry.name}.txt', "w")
        delim = '----------------------------------------------------------------------'

        # Print parse result.
        f.write(f'Source code:\n{delim}\n{code}{delim}\n\n')
        f.write(f'IR:\n{delim}\n{ir_orig_dump}{delim}\n\n')
        f.write(f'Optimized IR:\n{delim}\n{ir_opt_dump}{delim}\n\n')

        # Print run result.
        f.write(f'Run:\n{delim}\n')
        f.write(f'In data:\n')
        for x in input_data:
            f.write(f'{x}: {input_data[x]}\n')
        f.write(f'{delim}\n')
        f.write(f'Result orig:\n')
        for x in res_orig:
            f.write(f'{x}: {res_orig[x]}\n')
        f.write(f'Result opt:\n')
        for x in res_opt:
            f.write(f'{x}: {res_opt[x]}\n')
        f.write(f'Results compare:\n')
        for x in res_opt:
            f.write(f'{x}: diff = {np.array(res_orig[x]) - np.array(res_opt[x])}\n')
        f.write(f'{delim}\n')
        f.close()

# ==================================================================================================


if __name__ == '__main__':

    dump_all_cases()

# ==================================================================================================
