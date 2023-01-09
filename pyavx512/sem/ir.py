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

        raise Exception(f'py-avx512 : no input param {name}')

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

        raise Exception(f'py-avx512 : no output param {name}')

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

    def new_oper(self, name, args=[], res=None, predct=None, predct_v=True,
                 cur_node=None, oper_after=None):
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
        predct : sem.Operand
            Predicate.
        predct_v : Bool
            Value of predct to jump.

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
        oper.Predct = predct
        oper.PredctV = predct_v
        self.Opers.append(oper)

        if cur_node is None:
            self.CurNode.Opers.append(oper)
        else:
            if oper_after is None:
                index = 0
            else:
                index = cur_node.Opers.index(oper_after) + 1
            cur_node.Opers.insert(index, oper)

        return oper.Res

    # ----------------------------------------------------------------------------------------------

    def fload(self, src, predct=None, predct_v=True):
        """
        Create load operation.

        Parameters
        ----------
        src : sem.Operand
            Source of load.
        predct : sem.Operand
            Predicate.
        predct_v : Bool
            Value of predct to jump.

        Returns
        -------
            Result.
        """

        res = self.new_reg()

        self.new_oper('fload', args=[self.in_param(src)],
                      res=res, predct=predct, predct_v=predct_v)

        return res

    # ----------------------------------------------------------------------------------------------

    def fstore(self, v, dst, predct=None, predct_v=True):
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
        predct_v : Bool
            Value of predct to jump.
        """

        self.new_oper('fstore', args=[v, dst],
                      predct=predct, predct_v=predct_v)

    # ----------------------------------------------------------------------------------------------

    def fadd(self, v1, v2, predct=None, predct_v=True):
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
        predct_v : Bool
            Value of predct to jump.

        Returns
        -------
            Result.
        """

        res = self.new_reg()

        self.new_oper('fadd', args=[v1, v2],
                      res=res, predct=predct, predct_v=predct_v)

        return res

    # ----------------------------------------------------------------------------------------------

    def fsub(self, v1, v2, predct=None, predct_v=True):
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
        predct_v : Bool
            Value of predct to jump.

        Returns
        -------
            Result.
        """

        res = self.new_reg()

        self.new_oper('fsub', args=[v1, v2],
                      res=res, predct=predct, predct_v=predct_v)

        return res

    # ----------------------------------------------------------------------------------------------

    def fmul(self, v1, v2, predct=None, predct_v=True):
        """
        Create mul operation.

        Parameters
        ----------
        v1 : sem.Operand
            First operand.
        v2 : sem.Operand
            Second operand.
        predct : sem.Operand
            Predicate.
        predct_v : Bool
            Value of predct to jump.

        Returns
        -------
            Result.
        """

        res = self.new_reg()

        self.new_oper('fmul', args=[v1, v2],
                      res=res, predct=predct, predct_v=predct_v)

        return res

    # ----------------------------------------------------------------------------------------------

    def fpow(self, v1, v2, predct=None, predct_v=True):
        """
        Create pow operation.

        Parameters
        ----------
        v1 : sem.Operand
            First operand.
        v2 : sem.Operand
            Second operand.
        predct : sem.Operand
            Predicate.
        predct_v : Bool
            Value of predct to jump.

        Returns
        -------
            Result.
        """

        res = self.new_reg()

        self.new_oper('fpow', args=[v1, v2],
                      res=res, predct=predct, predct_v=predct_v)

        return res

    # ----------------------------------------------------------------------------------------------

    def fsqrt(self, v1, v2, predct=None, predct_v=True):
        """
        Create sqrt operation.

        Parameters
        ----------
        v1 : sem.Operand
            First operand.
        v2 : sem.Operand
            Second operand.
        predct : sem.Operand
            Predicate.
        predct_v : Bool
            Value of predct to jump.

        Returns
        -------
            Result.
        """

        res = self.new_reg()

        self.new_oper('sqrt', args=[v1, v2],
                      res=res, predct=predct, predct_v=predct_v)

        return res

    # ----------------------------------------------------------------------------------------------

    def fdiv(self, v1, v2, predct=None, predct_v=True):
        """
        Create div operation.

        Parameters
        ----------
        v1 : sem.Operand
            First operand.
        v2 : sem.Operand
            Second operand.
        predct : sem.Operand
            Predicate.
        predct_v : Bool
            Value of predct to jump.

        Returns
        -------
            Result.
        """

        res = self.new_reg()

        self.new_oper('fdiv', args=[v1, v2],
                      res=res, predct=predct, predct_v=predct_v)

        return res

    # ----------------------------------------------------------------------------------------------

    def fcmpge(self, v1, v2, predct=None, predct_v=True):
        """
        Create fcmpge operation.

        Parameters
        ----------
        v1 : sem.Operand
            First operand.
        v2 : sem.Operand
            Second operand.
        predct : sem.Operand
            Predicate.
        predct_v : Bool
            Value of predct to jump.

        Returns
        -------
            Result.
        """

        res = self.new_predicate()

        self.new_oper('fcmpge', args=[v1, v2],
                      res=res, predct=predct, predct_v=predct_v)

        return res

    # ----------------------------------------------------------------------------------------------

    def fcmplt(self, v1, v2, predct=None, predct_v=True):
        """
        Create fcmplt operation.

        Parameters
        ----------
        v1 : sem.Operand
            First operand.
        v2 : sem.Operand
            Second operand.
        predct : sem.Operand
            Predicate.
        predct_v : Bool
            Value of predct to jump.

        Returns
        -------
            Result.
        """

        res = self.new_predicate()

        self.new_oper('fcmplt', args=[v1, v2],
                      res=res, predct=predct, predct_v=predct_v)

        return res

    # ----------------------------------------------------------------------------------------------

    def fcmplte(self, v1, v2, predct=None, predct_v=True):
        """
        Create cmplt operation.

        Parameters
        ----------
        v1 : sem.Operand
            First operand.
        v2 : sem.Operand
            Second operand.
        predct : sem.Operand
            Predicate.
        predct_v : Bool
            Value of predct to jump.

        Returns
        -------
            Result.
        """

        res = self.new_predicate()

        self.new_oper('fcmplte', args=[v1, v2],
                      res=res, predct=predct, predct_v=predct_v)

        return res

    # ----------------------------------------------------------------------------------------------

    def fcmpeq(self, v1, v2, predct=None, predct_v=True):
        """
        Create fcmpeq operation.

        Parameters
        ----------
        v1 : sem.Operand
            First operand.
        v2 : sem.Operand
            Second operand.
        predct : sem.Operand
            Predicate.
        predct_v : Bool
            Value of predct to jump.

        Returns
        -------
            Result.
        """

        res = self.new_predicate()

        self.new_oper('fcmpeq', args=[v1, v2],
                      res=res, predct=predct, predct_v=predct_v)

        return res

    # ----------------------------------------------------------------------------------------------

    def pand(self, v1, v2, predct=None, predct_v=True):
        """
        Create logical and operation.

        Parameters
        ----------
        v1 : sem.Operand
            First operand.
        v2 : sem.Operand
            Second operand.
        predct : sem.Operand
            Predicate.
        predct_v : Bool
            Value of predct to jump.

        Returns
        -------
            Result.
        """

        res = self.new_predicate()

        self.new_oper('pand', args=[v1, v2],
                      res=res, predct=predct, predct_v=predct_v)

        return res

    # ----------------------------------------------------------------------------------------------

    def jump(self, target_node, predct=None, predct_v=True):
        """
        Create jump operation.

        Parameters
        ----------
        target_node : cfg.Node
            Node to jump.
        predct : sem.Operand
            Predicate.
        is_predct_inv : Bool
            Is predicate inversed.
        """

        self.new_oper('jump', predct=predct, predct_v=predct_v)
        self.CFG.new_edge(self.CurNode, target_node, self.CurNode.LastOper)

    # ----------------------------------------------------------------------------------------------

    def dump(self):
        s = f'\tin_params = {self.InParams}\n\tout_params = {self.OutParams}'
        return f'{s}\n\n{self.CFG.dump()}'

    # ----------------------------------------------------------------------------------------------

    def print(self):
        """
        Print.
        """

        print(self.dump())

# ==================================================================================================
