"""
Operand.
"""


# ==================================================================================================


class Operand:

    # ----------------------------------------------------------------------------------------------

    def __init__(self, kind, id):
        """
        Constructor.

        Parameters
        ----------
        kind : basestring
            Kind of operand.
        id : int | float | string
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
        self.Id = id

        # Producer (for result).
        self.Producer = None

        # Value for runtime.
        self.RuntimeVal = None

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
            return f'{self.Kind}/{self.Id}'
        elif self.Kind in ['r', 'p']:
            return f'{self.Kind}{self.Id}'
        elif self.Kind == 'c':
            return f'{self.Kind}.{self.Id}'
        else:
            raise Exception(f'unknown operand kind "{self.Kind}"')

# ==================================================================================================
