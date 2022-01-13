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

        # Node in which operations are created in this moment.
        self.CurNode = None

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

    def set_cur_node(self, node):
        """
        Set current node.

        Parameters
        ----------
        node : cfg.Node
            Node.
        """

        self.CurNode = node

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
            return max([p.Id for p in self.Predicates]) + 1

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

    def new_oper(self, name, args=[], res=None, predct=None, is_predct_inv=False):
        """
        Create new oper.

        Parameters
        ----------
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
        oper.Predicate = predct
        oper.IsInvertPredicate = is_predct_inv
        self.Opers.append(oper)
        self.CurNode.Opers.append(oper)

        return oper.Res

    # ----------------------------------------------------------------------------------------------

    def load(self, src, predct=None, is_predct_inv=False):
        """
        Create load operation.

        Parameters
        ----------
        src : sem.Operand
            Source of load.
        predct : sem.Operand
            Predicate.
        is_predct_inv : Bool
            Is predicate inversed.

        Returns
        -------
            Result.
        """

        res = self.new_reg()

        self.new_oper('load', args=[self.in_param(src)],
                      res=res, predct=predct, is_predct_inv=is_predct_inv)

        return res

    # ----------------------------------------------------------------------------------------------

    def store(self, v, dst, predct=None, is_predct_inv=False):
        """
        Create load operation.

        Parameters
        ----------
        v : sem.Operand
            Value.
        dst : sem.Operand
            Destination.
        predct : sem.Operand
            Predicate.
        is_predct_inv : Bool
            Is predicate inversed.
        """

        self.new_oper('store', args=[v, self.out_param(dst)],
                      predct=predct, is_predct_inv=is_predct_inv)

    # ----------------------------------------------------------------------------------------------

    def add(self, v1, v2, predct=None, is_predct_inv=False):
        """
        Create add operation.

        Parameters
        ----------
        v1 : sem.Operand
            First operand.
        v2 : sem.Operand
            Second operand.
        predct : sem.Operand
            Predicate.
        is_predct_inv : Bool
            Is predicate inversed.

        Returns
        -------
            Result.
        """

        res = self.new_reg()

        self.new_oper('add', args=[v1, v2],
                      res=res, predct=predct, is_predct_inv=is_predct_inv)

        return res

    # ----------------------------------------------------------------------------------------------

    def sub(self, v1, v2, predct=None, is_predct_inv=False):
        """
        Create sub operation.

        Parameters
        ----------
        v1 : sem.Operand
            First operand.
        v2 : sem.Operand
            Second operand.
        predct : sem.Operand
            Predicate.
        is_predct_inv : Bool
            Is predicate inversed.

        Returns
        -------
            Result.
        """

        res = self.new_reg()

        self.new_oper('sub', args=[v1, v2],
                      res=res, predct=predct, is_predct_inv=is_predct_inv)

        return res

    # ----------------------------------------------------------------------------------------------

    def cmpge(self, v1, v2, predct=None, is_predct_inv=False):
        """
        Create cmpge operation.

        Parameters
        ----------
        v1 : sem.Operand
            First operand.
        v2 : sem.Operand
            Second operand.
        predct : sem.Operand
            Predicate.
        is_predct_inv : Bool
            Is predicate inversed.

        Returns
        -------
            Result.
        """

        res = self.new_predicate()

        self.new_oper('cmpge', args=[v1, v2],
                      res=res, predct=predct, is_predct_inv=is_predct_inv)

        return res

    # ----------------------------------------------------------------------------------------------

    def jump(self, predct=None, is_predct_inv=False):
        """
        Create jump operation.

        Parameters
        ----------
        predct : sem.Operand
            Predicate.
        is_predct_inv : Bool
            Is predicate inversed.
        """

        self.new_oper('jump', predct=predct, is_predct_inv=is_predct_inv)

    # ----------------------------------------------------------------------------------------------

    def print(self):
        """
        Print.
        """

        print('IR:')
        print(f'  in_params = {self.InParams}, out_params = {self.OutParams}')

        self.CFG.print()

# ==================================================================================================
