# ==================================================================================================

class DependencyAnalyzer:

    # ----------------------------------------------------------------------------------------------

    def analyze(self, ir):

        opers_before = []
        preds_before = []
        nodes = [ir.CFG.StartNode]
        self.process(nodes, opers_before, preds_before)

    # ----------------------------------------------------------------------------------------------

    def process(self, nodes, opers_before, preds_before):
        for node in nodes:
            for oper in node.Opers:
                args = [oper.Predct] if oper.Name == 'jump' else oper.Args
                for arg in args:
                    pred_opers = self.find_opers_with_arg(arg, opers_before)
                    oper.PredOpers.extend(o for o in pred_opers if o not in oper.PredOpers and o != oper)

                    for o in pred_opers:
                        if oper not in o.SuccOpers and oper != o:
                            o.SuccOpers.append(oper)

                opers_before.append(oper)
                if oper.Res is not None and oper.Res.Kind == 'p':
                    preds_before.append(oper.Res)

                if oper.Name == 'jump':
                    to_node = next(edge.Succ for edge in node.OEdges if edge.Jump == oper)
                    if to_node.Opers[0] not in oper.SuccOpers:
                        oper.SuccOpers.append(to_node.Opers[0])
                    if oper not in to_node.Opers[0].PredOpers:
                        to_node.Opers[0].PredOpers.append(oper)

        jump_nodes = [edge.Succ for edge in node.OEdges for node in nodes]
        if len(jump_nodes) != 0:
            self.process(jump_nodes, opers_before, preds_before)

    # ----------------------------------------------------------------------------------------------

    def find_opers_with_arg(self, arg, opers):
        find_opers = []
        for oper in opers:
            if arg in oper.Args:
                find_opers.append(oper)

            if arg == oper.Res:
                find_opers.append(oper)

        return find_opers

    # ----------------------------------------------------------------------------------------------

# ==================================================================================================
