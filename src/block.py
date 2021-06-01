from mask import Mask
from zmm import ZMM
import operation
from operation import Operation

# ==================================================================================================

class Block:

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor.
        """

        self.Id = 0
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

    def op(self, name, args, pred=None, zflag=None):
        """
        Create new operation, create result for it,
        append to block operations list and return result.

        :param name: name of operation
        :param args: arguments list
        :param pred: predicate
        :param zflag: zero flag
        :return: operation result
        """

        # Create result.
        res_type = operation.operation_res_type(name)
        if res_type == 'm':
            res = self.CFG.alloc_mask()
        else:
            res = self.CFG.alloc_zmm(res_type)

        # Create operation.
        oper = Operation(name, args, res, pred, zflag)

        # Add operation to block operations list.
        self.add_operation(oper)

        return res

    # ----------------------------------------------------------------------------------------------

    def id_str(self):
        """
        String representation.

        :return: string
        """

        return 'Block {0}'.format(self.Id)

    # ----------------------------------------------------------------------------------------------

    def str_s(self):
        """
        Convert to string.

        :return: string representation
        """

        return self.id_str()

    # ----------------------------------------------------------------------------------------------

    def str_l(self):
        """
        Convert to string.

        :return: string representation
        """

        return self.id_str()

    # ----------------------------------------------------------------------------------------------

    def print_s(self):
        """
        Print short version.
        """

        print('Block {0} begin:'.format(self.Id))

        for oper in self.Operations:
            oper.print_s()

        print('Block {0} end.'.format(self.Id))

    # ----------------------------------------------------------------------------------------------

    def print_l(self):
        """
        Print long version.
        """

        print('Block {0} begin:'.format(self.Id))

        for oper in self.Operations:
            oper.print_l()

        print('Block {0} end.'.format(self.Id))

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
