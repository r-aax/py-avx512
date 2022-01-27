"""
Emulator realization.
"""

# ==================================================================================================
import math


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

    def run(self, ir, data):
        """
        Run emulator.

        Parameters
        ----------
        ir : sem.IR
            Intermediate representation.
        data
            Input data.

        Returns
        -------
            Output data.
        """

        cases = len(list(data.values())[0])

        print(f'tools:emulator : run {cases} cases with {data}')

        out_data = dict()

        for i in range(cases):

            # Init runtime values for input parameters.
            for in_p in ir.InParams:
                in_p.RuntimeVal = data[in_p.Id][i]

            for const in ir.Constants:
                const.RuntimeVal = float(const.Id)

            for out_p in ir.OutParams:
                out_p.RuntimeVal = None

            if self.debug:
                print('--InParams: ' + ', '.join(f'{d.Id} = {d.RuntimeVal}' for d in ir.InParams) + '--')

            self.single_run(ir)

            # Get output runtime values.
            for out_p in ir.OutParams:
                if out_data.get(out_p.Id) is None:
                    out_data[out_p.Id] = [out_p.RuntimeVal]
                else:
                    out_data[out_p.Id].append(out_p.RuntimeVal)

            if self.debug:
                print('--OutParams: ' + ', '.join(f'{d.Id} = {d.RuntimeVal}' for d in ir.OutParams) + '--')

        print(f'tools:emulator : ends with {out_data}')

        return out_data

    # ----------------------------------------------------------------------------------------------

    def single_run(self, ir):
        """
        Run with single set of data.

        Parameters
        ----------
        ir : sem.IR
            Intermediate representation.
        """

        cur_node = ir.CFG.StartNode
        cur_oper_i = 0

        # Emulate while we can do it.
        while True:
            # Check end of emulation.
            if cur_oper_i >= len(cur_node.Opers):
                break

            cur_oper = cur_node.Opers[cur_oper_i]
            print(cur_oper)
            self.emulate_oper(cur_oper)

            # Move to next operation.
            if cur_oper.is_runtime_jump():
                new_node = None
                for e in cur_node.OEdges:
                    if e.Jump == cur_oper:
                        new_node = e.Succ
                        break
                if new_node is None:
                    raise Exception('py-avx512 : jump operation {0} to nowhere'.format(str(cur_oper)))
                cur_node = new_node
                cur_oper_i = 0
            else:
                cur_oper_i += 1

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

        if n == 'load':
            oper.Res.RuntimeVal = oper.Args[0].RuntimeVal

        elif n == 'eq':
            oper.Res.RuntimeVal = oper.Args[0].RuntimeVal == oper.Args[1].RuntimeVal
        elif n == 'cmpge':
            oper.Res.RuntimeVal = oper.Args[0].RuntimeVal > oper.Args[1].RuntimeVal
        elif n == 'cmplt':
            oper.Res.RuntimeVal = oper.Args[0].RuntimeVal < oper.Args[1].RuntimeVal
        elif n == 'cmplte':
            oper.Res.RuntimeVal = oper.Args[0].RuntimeVal <= oper.Args[1].RuntimeVal
        elif n == 'l_and':
            oper.Res.RuntimeVal = oper.Args[0].RuntimeVal and oper.Args[1].RuntimeVal

        elif n == 'add':
            oper.Res.RuntimeVal = oper.Args[0].RuntimeVal + oper.Args[1].RuntimeVal
        elif n == 'sub':
            oper.Res.RuntimeVal = oper.Args[0].RuntimeVal - oper.Args[1].RuntimeVal
        elif n == 'mul':
            oper.Res.RuntimeVal = oper.Args[0].RuntimeVal * oper.Args[1].RuntimeVal
        elif n == 'div':
            oper.Res.RuntimeVal = oper.Args[0].RuntimeVal / oper.Args[1].RuntimeVal if oper.Args[
                                                                                           1].RuntimeVal != 0 else float(
                'inf')

        elif n == 'pow':
            oper.Res.RuntimeVal = math.pow(oper.Args[0].RuntimeVal, oper.Args[1].RuntimeVal)
        elif n == 'sqrt':
            oper.Res.RuntimeVal = math.sqrt(oper.Args[0].RuntimeVal)

        elif n == 'unary_minus':
            oper.Res.RuntimeVal = -oper.Args[0].RuntimeVal

        elif n == 'jump':
            # Jump operation has no calc semantic.
            pass
        elif n == 'nop':
            # Empty operation.
            pass
        elif n == 'store':
            if self.debug:
                print('store', oper.Args[1], oper.Args[1].RuntimeVal, oper.Args[0], oper.Args[0].RuntimeVal)

            oper.Args[1].RuntimeVal = oper.Args[0].RuntimeVal
        else:
            raise Exception('py-avx512 : unknown operation {0}'.format(oper))

        if self.debug and len(oper.Args) > 1 and oper.Res is not None:
            print(n, f'{oper.Args[0]}={oper.Args[0].RuntimeVal}', f'{oper.Args[1]}={oper.Args[1].RuntimeVal} ->',
                  f'{oper.Res}={oper.Res.RuntimeVal}')

# ==================================================================================================
