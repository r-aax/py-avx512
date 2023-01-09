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
        self.OptAction =\
            {
                'cond_opt': self.cond_opt,
                'merge': self.merge,
                'low_prob': self.low_prob,
                'predct': self.predct
            }

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

    # ----------------------------------------------------------------------------------------------

    def merge(self, ir):

        # For each edge add oper por into begin of node.
        for edge in ir.CFG.Edges:
            jump_oper = edge.Jump
            p = jump_oper.Predct
            oname = 'pmov' if jump_oper.PredctV else 'pnot'
            res = ir.new_predicate()
            succ_node = edge.Succ
            ir.new_oper(oname, args=[p], res=res, predct=None, predct_v=True,
                        cur_node=succ_node, oper_after=None)

            oi = 1
            while True:
                if oi >= len(succ_node.Opers):
                    break
                op = succ_node.Opers[oi]
                if op.Predct is None:
                    op.Predct = res
                    op.PredctV = True
                    oi += 1
                    continue
                else:
                    # Make new predicate generation operation and shift io on 2.
                    producer = op.Predct.Producer
                    oname2 = 'pand' if op.PredctV else 'pandn'
                    res2 = ir.new_predicate()
                    ir.new_oper(oname2, args=[res, op.Predct], res=res2, predct=None, predct_v=True,
                                cur_node=succ_node, oper_after=producer)
                    op.Predct = res2
                    op.PredctV = True
                    oi += 2
                    continue

        # Now we can delete all nodes.
        new_opers = []
        for node in ir.CFG.Nodes:
            for op in node.Opers:
                if op.Name != 'jump':
                    op.Counter = node.Counter
                    new_opers.append(op)
        start_node = ir.CFG.Nodes[0]
        start_node.IEdges = []
        start_node.OEdges = []
        start_node.Opers = new_opers
        ir.CFG.Nodes = [start_node]
        ir.CFG.Edges = []
        ir.Opers = new_opers

    def low_prob(self, ir):
        start_node = ir.CFG.Nodes[0]
        start_node.Opers = [op for op in start_node.Opers if op.Counter > 0]
        ir.Opers = start_node.Opers

    def predct(self, ir):
        opers = ir.Opers
        for p in ir.Predicates:
            producer = p.Producer
            if producer.Name == 'pmov':
                new_p = producer.Args[0]
                for op in opers:
                    for ai in range(len(op.Args)):
                        if op.Args[ai] == p:
                            op.Args[ai] = new_p
                    if op.Predct == p:
                        op.Predct = new_p
                if producer in opers:
                    opers.remove(producer)
        ir.Opers = opers
        ir.CFG.Nodes[0].Opers = opers

# ==================================================================================================
