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


def write_and_close(filename, content):
    """
    Open file, write content to it and close.

    Parameters
    ----------
    filename : str
        Name of file.
    content : str
        Content.
    """

    with open(filename, 'w') as f:
        f.write(content)
        f.close()

# ==================================================================================================


def write_input_and_res_data(f, input_data, res, res_orig, oc, oc_orig, detail_print=False):
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
    oc : int
        Opers count.
    oc_orig : int
        Origin opers count.
    detail_print : bool
        Flag for detail print.
    """

    f.write('\n\n=================================\n')

    if detail_print:
        f.write(f'Input Data:\n')
        for x in input_data:
            f.write(f'\t{x} : {input_data[x]}\n')
        f.write('Result Data:\n')
        for x in res:
            f.write(f'\t{x} : {np.array(res[x])}\n')
            f.write(f'\t{x} : {np.array(res_orig[x])}\n')

    def xdiff(x, y):
        if (x is None) or (y is None):
            return 'Nan'
        else:
            return x - y

    f.write(f'Results compare:\n')
    for x in res:
        f.write(f'\t{x}: diff = {[xdiff(k, z) for k, z in zip(np.array(res[x]), np.array(res_orig[x]))]}\n')
    f.write('Speedup:\n')
    f.write(f'\toc = {oc}\n\torig_oc = {oc_orig}\n\tspeedup = {oc_orig / oc}\n')

# ==================================================================================================


def dump_cases(cases=None,
               black_hole=True):
    """
    Run cases.

    Parameters
    ----------
    cases
        Names of cases for run.
    """

    # Paths for cases and out dir.
    cases_path, out_path = 'cases', 'out'

    # Parser, optimizer, emulator, dependency analyzer.
    parser = sem.Parser()
    optimizer = tools.Optimizer()
    emulator = tools.Emulator()
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
            input_data[in_param.Id] = np.random.uniform(1.0, 2.0, 100)
        # Emulate right results.
        res_orig, oc_orig = emulator.run(ir, input_data)
        with open(f'{dst_dir}/{case}_01_parse.txt', 'w') as f:
            f.write(ir.dump())
            write_input_and_res_data(f, input_data, res_orig, res_orig, oc_orig, oc_orig)
            f.close()

        # 02 and sso on..
        # Optimization.
        optimizer.set_cur_phase_number(1)
        if black_hole:
            phases = ['merge', 'low_prob', 'predct']
        else:
            phases = ['merge', 'predct']
        for opt_name in phases:
            optimizer.optimize(ir, opt_name)
            res, oc = emulator.run(ir, input_data, reset_profile=True)
            with open(f'{dst_dir}/{case}_{optimizer.CurPhaseNumber:02}_{opt_name}.txt', 'w') as f:
                f.write(ir.dump())
                write_input_and_res_data(f, input_data, res, res_orig, oc, oc_orig)
                f.close()

        # Generation of the code.
        optimizer.CurPhaseNumber += 1
        with open(f'{dst_dir}/{case}_{optimizer.CurPhaseNumber:02}_cg.txt', 'w') as f:
            tools.codegenerator.cg(f, ir)
            f.close()

        run_stat[case] = f'OK (speedup {oc_orig / oc})'

    # Stat.
    print('Stat:')
    for x in run_stat:
        print(f'\t{x} : {run_stat[x]}')

# ==================================================================================================


if __name__ == '__main__':

    dump_cases(cases=None,
               black_hole=True)

# ==================================================================================================
