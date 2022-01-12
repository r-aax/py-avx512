"""
Operand.
"""

# ==================================================================================================


class Operand:

    # ----------------------------------------------------------------------------------------------

    def __init__(self, kind, val):
        """
        Constructor.

        Parameters
        ----------
        kind : basestring
            Kind of operand.
        val : int | float
            Number.
        """

        self.Kind = kind
        self.Val = val

    # ----------------------------------------------------------------------------------------------

    @property
    def Num(self):
        """
        Number (usefull for virtual registers and predicates).

        Returns
        -------
        num : int
            Number
        """

        return self.Val

# ==================================================================================================
