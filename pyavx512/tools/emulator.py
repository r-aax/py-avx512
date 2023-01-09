"""
Emulator realization.
"""

import math


# ==================================================================================================


class Emulator:
    """
    Emulator.
    """

    # ----------------------------------------------------------------------------------------------

    def __init__(self, debug=False):
        """
        Constructor.
        """

        self.debug = debug

        pass

    # ----------------------------------------------------------------------------------------------

    def run(self, ir, data, reset_profile=False):
        """
        Run emulator.

        Parameters
        ----------
        ir : sem.IR
            Intermediate representation.
        data : dictionary
            Input data.
            Format if input data : { <name of parameter>: <array of values> }
        reset_profile : Bool
            Reset profile before run or not.

        Returns
        -------
            Output data and emulated operations count
            (tuple { data, opers_count }).
        """

        if reset_profile:
            ir.CFG.reset_profile()

        emulated_operations_count = 0
        cases = len(list(data.values())[0])

        # print(f'tools:emulator : run {cases} cases with {data}')

        out_data = dict()

        for i in range(cases):

            # Init runtime values for input parameters.
            for in_p in ir.InParams:
                in_p.Val = data[in_p.Id][i]

            for const in ir.Constants:
                const.Val = float(const.Id)

            for out_p in ir.OutParams:
                out_p.Val = None

            if self.debug:
                print('--InParams: ' + ', '.join(f'{d.Id} = {d.Val}' for d in ir.InParams) + '--')

            try:
                emulated_operations_count += self.single_run(ir)
            except Exception as e:
                print(e)

            # Get output runtime values.
            for out_p in ir.OutParams:
                if out_data.get(out_p.Id) is None:
                    out_data[out_p.Id] = [out_p.Val]
                else:
                    out_data[out_p.Id].append(out_p.Val)

            if self.debug:
                print('--OutParams: ' + ', '.join(f'{d.Id} = {d.Val}' for d in ir.OutParams) + '--')

        # print(f'tools:emulator : ends with {out_data}')

        return out_data, emulated_operations_count

    # ----------------------------------------------------------------------------------------------

    def single_run(self, ir):
        """
        Run with single set of data.

        Parameters
        ----------
        ir : sem.IR
            Intermediate representation.

        Returns
        -------
            Emulated operations count.
        """

        emulated_operations_count = 0

        cur_node = ir.CFG.StartNode
        cur_node.Counter += 1
        cur_oper_i = 0

        # Emulate while we can do it.
        while True:
            # Check end of emulation.
            if cur_oper_i >= len(cur_node.Opers):
                break

            cur_oper = cur_node.Opers[cur_oper_i]
            # print(cur_oper)
            self.emulate_oper(cur_oper)
            emulated_operations_count += 1

            # Move to next operation.
            if cur_oper.is_runtime_jump():
                new_node = None
                for e in cur_node.OEdges:
                    if e.Jump == cur_oper:
                        e.Counter += 1
                        new_node = e.Succ
                        break
                if new_node is None:
                    raise Exception('py-avx512 : jump operation {0} to nowhere'.format(str(cur_oper)))
                cur_node = new_node
                cur_node.Counter += 1
                cur_oper_i = 0
            else:
                cur_oper_i += 1

        return emulated_operations_count

    # ----------------------------------------------------------------------------------------------

    def emulate_oper(self, oper):
        """
        Emulate operation.

        Parameters
        ----------
        oper : sem.Oper
            Operation.
        """

        n = oper.Name

        if n == 'fload':
            oper.Res.Val = oper.Args[0].Val

        elif n == 'fcmpeq':
            oper.Res.Val = oper.Args[0].Val == oper.Args[1].Val
        elif n == 'fcmpge':
            oper.Res.Val = oper.Args[0].Val > oper.Args[1].Val
        elif n == 'fcmplt':
            oper.Res.Val = oper.Args[0].Val < oper.Args[1].Val
        elif n == 'fcmplte':
            oper.Res.Val = oper.Args[0].Val <= oper.Args[1].Val
        elif n == 'pand':
            oper.Res.Val = oper.Args[0].Val and oper.Args[1].Val

        elif n == 'fadd':
            oper.Res.Val = oper.Args[0].Val + oper.Args[1].Val
        elif n == 'fsub':
            oper.Res.Val = oper.Args[0].Val - oper.Args[1].Val
        elif n == 'fmul':
            oper.Res.Val = oper.Args[0].Val * oper.Args[1].Val
        elif n == 'fmin':
            oper.Res.Val = min(oper.Args[0].Val, oper.Args[1].Val)
        elif n == 'fmax':
            oper.Res.Val = max(oper.Args[0].Val, oper.Args[1].Val)
        elif n == 'fdiv':
            oper.Res.Val = oper.Args[0].Val / oper.Args[1].Val if oper.Args[1].Val != 0 else float('inf')

        elif n == 'fpow':
            try:
                oper.Res.Val = math.pow(oper.Args[0].Val, oper.Args[1].Val)
            except ValueError as e:
                print(e)
                oper.Res.Val = math.nan
        elif n == 'fsqrt':
            oper.Res.Val = math.sqrt(oper.Args[0].Val)

        elif n == 'unary_minus':
            oper.Res.Val = -oper.Args[0].Val

        elif n == 'fmov':
            oper.Args[1].Val = oper.Args[0].Val
        elif n == 'jump':
            # Jump operation has no calc semantic.
            pass
        elif n == 'nop':
            # Empty operation.
            pass
        elif n == 'fstore':
            oper.Args[1].Val = oper.Args[0].Val
        elif n == 'pmov':
            oper.Res.Val = oper.Args[0].Val
        elif n == 'pnot':
            oper.Res.Val = not oper.Args[0].Val
        elif n == 'por':
            oper.Res.Val = oper.Args[0].Val or oper.Args[1].Val
        elif n == 'pand':
            oper.Res.Val = oper.Args[0].Val and oper.Args[1].Val
        elif n == 'pandn':
            oper.Res.Val = oper.Args[0].Val and not oper.Args[1].Val
        else:
            raise Exception('py-avx512 : unknown operation {0}'.format(oper))

        if self.debug:
            print(n, ', '.join(f'{k}={k.Val}' for k in oper.Args),
                  f'{oper.Res}={oper.Res.Val}' if oper.Res is not None else '')

# ==================================================================================================
