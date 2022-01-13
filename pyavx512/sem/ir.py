"""
Intermediate representation.
"""

import sem
import cfg

# ==================================================================================================


class IR:
    """
    Intermediate representation.
    """

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor.
        """

        # CFG
        self.CFG = cfg.Graph()

        # In params.
        self.InParams = []

        # Out params.
        self.OutParams = []

        # Registers.
        self.Regs = []

        # Predicates.
        self.Predicates = []

        # Constants.
        self.Constants = []

        # Operations list.
        self.Opers = []

    # ----------------------------------------------------------------------------------------------

    def set_in_out_params(self, in_params, out_params):
        """
        Set input and output parameters.

        Parameters
        ----------
        in_params : list
            List of input parameters.
        out_params : list
            List of output parameters.
        """

        self.InParams = [sem.Operand('i', name) for name in in_params]
        self.OutParams = [sem.Operand('o', name) for name in out_params]

    # ----------------------------------------------------------------------------------------------

    def new_reg_num(self):
        """
        Get number for new register.

        Returns
        -------
        id : int
            Number for new register.
        """

        if not self.Regs:
            return 0
        else:
            return max([r.Id for r in self.Regs]) + 1

    # ----------------------------------------------------------------------------------------------

    def new_predicate_num(self):
        """
        Get number for new predicate.

        Returns
        -------
        id : int
            Identifier for new predicate.
        """

        if not self.Predicates:
            return 0
        else:
            return max([p.Num for p in self.Predicates]) + 1

    # ----------------------------------------------------------------------------------------------

    def in_param(self, name):
        """
        Get input param.

        Parameters
        ----------
        name : string
            Input param.

        Returns
        -------
        param : Operand.
            Input param.
        """

        for in_par in self.InParams:
            if in_par.Id == name:
                return in_par

        raise Exception(f'py-avx512 : no input param{name}')

    # ----------------------------------------------------------------------------------------------

    def out_param(self, name):
        """
        Get output param.

        Parameters
        ----------
        name : string
            Output param.

        Returns
        -------
        param : Operand.
            Output param.
        """

        for out_par in self.OutParams:
            if out_par.Id == name:
                return out_par

        raise Exception(f'py-avx512 : no output param{name}')

    # ----------------------------------------------------------------------------------------------

    def new_reg(self):
        """
        Get new register.

        Returns
        -------
        reg : Operand
            Register.
        """

        r = sem.Operand('r', self.new_reg_num())
        self.Regs.append(r)

        return r

    # ----------------------------------------------------------------------------------------------

    def new_predicate(self):
        """
        Get new predicate.

        Returns
        -------
        predicate : Operand
            Predicate.
        """

        p = sem.Operand('p', self.new_predicate_num())
        self.Predicates.append(p)

        return p

    # ----------------------------------------------------------------------------------------------

    def new_constant(self, val):
        """
        Get new constant.

        Parameters
        ----------
        val : number
            Constant.

        Returns
        -------
            New constant operand.
        """

        c = sem.Operand('c', val)
        self.Constants.append(c)

        return c

    # ----------------------------------------------------------------------------------------------

    def new_oper_id(self):
        """
        Get identifier for new operation.

        Returns
        -------
        id : int
            Identifier for new operation.
        """

        if not self.Opers:
            return 0
        else:
            return max([oper.Id for oper in self.Opers]) + 1

    # ----------------------------------------------------------------------------------------------

    def new_oper(self, cfg_node, name, args=[], res=None, predicate=None, is_invert_predicate=False):
        """
        Create new oper.

        Parameters
        ----------
        cfg_node : cfg.Node
            Node.
        name : str
            Name.
        args : list
            Arguments.
        res : Operand
            Result.
        predicate :
            Predicate.

        Returns
        -------
            Operation.
        """

        oper = sem.Oper(self)
        oper.Name = name
        oper.Args = args
        oper.Res = res
        if res:
            res.Producer = oper
        oper.Predicate = predicate
        oper.IsInvertPredicate = is_invert_predicate
        self.Opers.append(oper)
        cfg_node.Opers.append(oper)

        return oper

    # ----------------------------------------------------------------------------------------------

    def print(self):
        """
        Print.
        """

        print('IR:')
        print(f'  in_params = {self.InParams}, out_params = {self.OutParams}')

        self.CFG.print()

# ==================================================================================================
