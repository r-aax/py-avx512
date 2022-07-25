"""
Operation.
"""


# ==================================================================================================


class Oper:

    # ----------------------------------------------------------------------------------------------

    def __init__(self, ir):
        """
        Constructor.

        Parameters
        ----------
        ir : sem.IR
            Intermediate representation.
        """

        self.IR = ir

        # Id.
        self.Id = ir.new_oper_id()

        # Name.
        self.Name = ''

        # Operation can have several arguments, one result and one predicate.
        self.Args = []
        self.Result = None
        self.Predct = None
        self.PredctV = True
        self.PredOpers = []
        self.SuccOpers = []

    # ----------------------------------------------------------------------------------------------

    def __repr__(self):
        """
        String representation.

        Returns
        -------
        str : str
            String.
        """

        # Issue #6.
        id_str, name_str = self.get_id(), self.get_name()
        if self.Args:
            args_str = ', '.join(['{0:>4}'.format(str(a)) for a in self.Args])
        else:
            args_str = ''
        if self.Res:
            res_str = '-> {0:>4}'.format(str(self.Res))
        else:
            res_str = ''
        if self.Predct:
            if not self.PredctV:
                s = '!'
            else:
                s = ' '
            tmp = '{0}{1}'.format(s, str(self.Predct))
            predct_str = '? {0:>4}'.format(tmp)
        else:
            predct_str = ''

        pred_opers = ', '.join(f'{pred.get_id()} {pred.get_name()}' for pred in self.PredOpers)
        succ_opers = ', '.join(f'{succ.get_id()} {succ.get_name()}' for succ in self.SuccOpers)

        return f'{id_str} {name_str} {args_str:12} {res_str:7} {predct_str:8} (pred = [{pred_opers}], succ = [{succ_opers}])'

    # ----------------------------------------------------------------------------------------------

    def get_name(self):
        return f'{self.Name:5}'

    # ----------------------------------------------------------------------------------------------

    def get_id(self):
        return f'{self.Id:2d}.'

    # ----------------------------------------------------------------------------------------------

    def is_runtime_jump(self):
        """
        Check if oper is jump.

        Returns
        -------
        is_jump : Bool
            True - if oper is jump,
            False - otherwinse.
        """

        if not self.Name == 'jump':
            return False

        if self.Predct is None:
            return True

        return self.PredctV == self.Predct.Val

# ==================================================================================================
