"""
Optimizer realization.
"""

import sem


# ==================================================================================================


class Optimizer:
    """
    Optimizer.
    """

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor.
        """

        self.CurPhaseNumber = 0
        self.OptAction = {"cond_opt": self.cond_opt}

    # ----------------------------------------------------------------------------------------------

    def set_cur_phase_number(self, cur_phase_number):
        """
        Set currect phase number.

        Parameters
        ----------
        cur_phase_number
            Phase number.
        """

        self.CurPhaseNumber = cur_phase_number

    # ----------------------------------------------------------------------------------------------

    def optimize(self, ir, optimization_name):
        """
        Process of optimization.

        Parameters
        ----------
        ir
            Intermediate representation.
        optimization_name
            Name of optimization phase.
        """

        self.CurPhaseNumber += 1
        if optimization_name in self.OptAction:
            self.OptAction[optimization_name](ir)

    # ----------------------------------------------------------------------------------------------
    def cond_opt(self, ir):
        """
        Remove cmpge operators with constants.

        Parameters
        ----------
        ir
            Intermediate representation.
        """
        opers = [oper for oper in ir.Opers if self.is_const_cmpge(oper)]

        opers.extend([oper for node in ir.CFG.Nodes for oper in node.Opers if self.is_const_cmpge(oper)])
        opers.sort(key=lambda c: c.Id, reverse=True)
        deleted_oper_ids = []

        for oper in opers:
            oper.SuccOpers[0].PredOpers = []
            if oper in ir.Opers: ir.Opers.remove(oper)
            if oper.Id not in deleted_oper_ids: deleted_oper_ids.append(oper.Id)

            opers_to_change_id = [i for i in ir.Opers if i.Id > oper.Id]
            for i in opers_to_change_id:
                i.Id -= 1

        for node in ir.CFG.Nodes:
            opers = list(node.Opers)
            for oper in opers:
                if oper.Id in deleted_oper_ids: node.Opers.remove(oper)

    def is_const_cmpge(self, oper):
        return oper.Name == 'fcmpge' and all(arg.Kind == 'c' for arg in oper.Args) and len(oper.SuccOpers) > 0
# ==================================================================================================
