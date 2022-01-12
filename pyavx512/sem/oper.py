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

        return f'{self.Id}. {self.Name} {self.Args} -> {self.Res} ? {self.Predicate}, {self.IsInvertPredicate}'

# ==================================================================================================
