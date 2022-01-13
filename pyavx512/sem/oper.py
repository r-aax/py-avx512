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
        self.Predicate = None
        self.IsInvertPredicate = False

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
        id_str = f'{self.Id:2d}.'
        name_str = f'{self.Name:5}'
        if self.Args:
            args_str = ', '.join(['{0:>4}'.format(str(a)) for a in self.Args])
        else:
            args_str = ''
        if self.Res:
            res_str = '-> {0:>4}'.format(str(self.Res))
        else:
            res_str = ''
        if self.Predicate:
            if self.IsInvertPredicate:
                s = '!'
            else:
                s = ' '
            tmp = '{0}{1}'.format(s, str(self.Predicate))
            predct_str = '? {0:>4}'.format(tmp)
        else:
            predct_str =''

        return f'{id_str} {name_str} {args_str:12} {res_str:7} {predct_str:8}'

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

        if self.Predicate is None:
            return True

        if not self.IsInvertPredicate:
            return self.Predicate.RuntimeVal
        else:
            return not self.Predicate.RuntimeVal

# ==================================================================================================
