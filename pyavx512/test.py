"""
Test file.
"""

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

    parser = sem.Parser()

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
            cfg, ir = parser.parse(entry.path)
            ir_dump = ir.dump()
        except Exception as e:
            ir_dump = f'Err: {e}'

        f = open(f'{output_path}/{entry.name}.txt', "w")
        delim = '----------------------------------------------------------------------'
        f.write(f'Source code:\n{delim}\n{code}{delim}\n\n')
        f.write(f'IR:\n{delim}\n{ir_dump}{delim}\n\n')
        opt = tools.Optimizer()
        opt.optimize(ir)
        opt_ir_dump = ir.dump()
        f.write(f'Optimized IR:\n{delim}\n{opt_ir_dump}{delim}\n')
        f.close()

# ==================================================================================================


if __name__ == '__main__':

    dump_all_cases(['001_if'])

# ==================================================================================================
