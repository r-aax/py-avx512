"""
Operation.
"""

from enum import Enum

# ==================================================================================================


class OperType(Enum):
    """
    Oper type.
    """

    # BEGIN - first operation of any node.
    BEGIN = 1001,

    # END - last operation of any node.
    END = 1002

# ==================================================================================================


class Oper:
    """
    Oper class.
    """

    # ----------------------------------------------------------------------------------------------

    def __init__(self, id, type):
        """
        Constructor.

        Parameters
        ----------
        id : int
            Identifier.
        type : OperType
            Operation type.
        """

        self.Type = type

# ==================================================================================================
