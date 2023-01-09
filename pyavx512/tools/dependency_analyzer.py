# ==================================================================================================

class DependencyAnalyzer:

    # ----------------------------------------------------------------------------------------------

    def analyze(self, ir):

        for node in ir.CFG.Nodes:

            # Clear.
            for o1 in node.Opers:
                o1.PredOpers = []
                o1.SuccOpers = []

            # Rebuld.
            for o1 in node.Opers:
                if o1.Res is not None:
                    for o2 in node.Opers:
                        if o2 != o1:
                            if (o1.Res in o2.Args) or (o1.Res == o2.Predct):
                                o1.SuccOpers.append(o2)
                                o2.PredOpers.append(o1)

# ==================================================================================================
