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
        val : int | float | string
            Number.
        """

        # Kind can be one of the following:
        #   i - input parametere
        #   o - output parameter
        #   r - register
        #   p - predicate
        #   c - constant
        self.Kind = kind

        # Value.
        self.Val = val

    # ----------------------------------------------------------------------------------------------

    def __repr__(self):
        """
        String representation of operand.

        Returns
        -------
        str : basestring
            String.
        """

        if self.Kind in ['i', 'o']:
            return f'{self.Val}/{self.Kind}'
        else:
            return f'{self.Kind}{self.Val}'

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
