"""
Test file.
"""

import numpy as np
import os
import sem
import tools
import shutil
from tools.dependency_analyzer import DependencyAnalyzer

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


def run_case(name, input=None, result=None):
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
    cfg, ir = parser.parse(f'cases/{name}.c')
    dep_analyzer = DependencyAnalyzer()
    dep_analyzer.analyze(ir)

    ir.print()
    emu = tools.Emulator(True)

    if input is None:
        return

    data = emu.run(ir, input)

    if result is None:
        return

    for k, v in result.items():
        for i in range(len(v)):
            is_close(result[k][i], data[k][i], k)

# ==================================================================================================


def write_and_close(filename, content):
    """
    Open file, write content to it and close.

    Parameters
    ----------
    filename
        Name of file.
    content
        Content.
    """

    with open(filename, 'w') as f:
        f.write(content)
        f.close()

# ==================================================================================================


def write_input_and_res_data(f, input_data, res, res_orig, oc, oc_orig):
    """
    Write IO statistics to file.

    Parameters
    ----------
    f
        File.
    input_data
        Input data.
    res
        Result.
    res_orig
        Origin result.
    oc
        Opers count.
    oc_orig
        Origin opers count.
    """
    delim = '================================='
    f.write(f'\n\n{delim}\nInput Data:\n')
    for x in input_data:
        f.write(f'\t{x} : {input_data[x]}\n')
    f.write('Result Data:\n')
    for x in res:
        f.write(f'\t{x} : {np.array(res[x])}\n')
        f.write(f'\t{x} : {np.array(res_orig[x])}\n')
    f.write(f'Results compare:\n')
    for x in res:
        f.write(f'\t{x}: diff = {[k - z if k is not None and z is not None else "Nan" for k, z in zip(np.array(res[x]), np.array(res_orig[x]))]}\n')
    f.write('Speedup:\n')
    f.write(f'\toc = {oc}\n\torig_oc = {oc_orig}\n\tspeedup = {oc_orig / oc}\n')

# ==================================================================================================


def dump_cases(cases=None):
    """
    Run cases.

    Parameters
    ----------
    cases
        Names of cases for run.
    """

    # Paths for cases and out dir.
    cases_path, out_path = 'cases', 'out'

    # Parser, optimizer and emulator.
    parser, optimizer, emulator = sem.Parser(), tools.Optimizer(), tools.Emulator()
    # Dependency analyzer.
    dep_analyzer = DependencyAnalyzer()

    # Scan cases folder and collect all names to run.
    run_cases = [e.name.split('.')[0] for e in os.scandir(cases_path) if e.name.endswith('.c')]
    if cases is not None:
        run_cases = [case for case in run_cases if case in cases]

    # Run stat.
    run_stat = {}

    # Run all cases.
    for case in run_cases:

        # Source file name.
        src_path = f'{cases_path}/{case}.c'

        # New dir name.
        dst_dir = f'{out_path}/{case}'
        if not os.path.isdir(dst_dir):
            os.makedirs(dst_dir)

        # 00 - source code.
        shutil.copy(src_path, f'{dst_dir}/{case}_00_source.txt')

        # 01 - parse.
        try:
            _, ir = parser.parse(src_path)
            dep_analyzer.analyze(ir)
        except Exception as e:
            print(e)
            write_and_close(f'{dst_dir}/{case}_01_parse.txt', f'Err: {e}')
            run_stat[case] = 'PARSE_ERROR'
            continue
        # Generate input data.
        input_data = {}
        for in_param in ir.InParams:
            input_data[in_param.Id] = np.random.uniform(-100.0, 100.0, 16)
        # Emulate right results.
        res_orig, oc_orig = emulator.run(ir, input_data)
        with open(f'{dst_dir}/{case}_01_parse.txt', 'w') as f:
            f.write(ir.dump())
            write_input_and_res_data(f, input_data, res_orig, res_orig, oc_orig, oc_orig)
            f.close()

        # 02 and sso on..
        # Optimization.
        optimizer.set_cur_phase_number(1)
        for opt_name in ['cond_opt', 'cg']:
            optimizer.optimize(ir, opt_name)
            res, oc = emulator.run(ir, input_data, reset_profile=True)
            with open(f'{dst_dir}/{case}_{optimizer.CurPhaseNumber:02}_{opt_name}.txt', 'w') as f:
                f.write(ir.dump())
                write_input_and_res_data(f, input_data, res, res_orig, oc, oc_orig)
                f.close()
        run_stat[case] = 'OK'

    # Stat.
    print('Stat:')
    for x in run_stat:
        print(f'\t{x} : {run_stat[x]}')

# ==================================================================================================


if __name__ == '__main__':

    dump_cases()

# ==================================================================================================
