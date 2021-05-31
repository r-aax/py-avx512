
# ==================================================================================================

class Block:

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor.
        """

        self.Operations = []

    # ----------------------------------------------------------------------------------------------

    def add_operation(self, operation):
        """
        Add operation.

        :param operation: operation
        """

        operation.Id = len(self.Operations)
        self.Operations.append(operation)

    # ----------------------------------------------------------------------------------------------

    def print_s(self):
        """
        Print short version.
        """

        for oper in self.Operations:
            oper.print_s()

    # ----------------------------------------------------------------------------------------------

    def print_l(self):
        """
        Print long version.
        """

        for oper in self.Operations:
            oper.print_l()

    # ----------------------------------------------------------------------------------------------

    def emulate(self, i):
        """
        Emulate all operations in the block.

        :param i: index
        """

        for oper in self.Operations:
            oper.emulate(i)

    # ----------------------------------------------------------------------------------------------

    def emulate_all(self):
        """
        Emualte all operations in all indices.
        """

        for oper in self.Operations:
            oper.emulate_all()

# ==================================================================================================
