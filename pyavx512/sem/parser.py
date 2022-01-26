from pycparser import parse_file, c_generator
import os
import sem


class Parser:

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        self.variable_counter = 0
        self.ir = sem.IR()
        self.cfg = self.ir.CFG
        self.variables = dict()
        self.nodes_before = []
        self.math_oper = {
            '+': self.ir.add,
            '-': self.ir.sub,
            '*': self.ir.mul,
            '/': self.ir.div
        }
        self.compare_oper = {
            '>': self.ir.cmpge,
            '<': self.ir.cmplt,
            '<=': self.ir.cmplte,
            '>=': self.ir.cmpge,
            '==': self.ir.eq,
        }

    # ----------------------------------------------------------------------------------------------

    def parse(self, path):
        src = os.path.abspath(path)
        ast = parse_file(src)  # , cpp_path='C:\\MinGW\\bin\\cpp.exe',use_cpp=True)
        body = ast.ext[0].body
        in_params = [k.name for k in ast.ext[0].decl.type.args.params if get_type(k.type) == 'TypeDecl']
        out_params = [k.name for k in ast.ext[0].decl.type.args.params if get_type(k.type) == 'PtrDecl']
        self.ir.set_in_out_params(in_params, out_params)

        for item in body.block_items:
            if get_type(item) != 'If':
                raise Exception('Not implemented')

            self.create_if_node(item)
            self.fill_edges_if_need()

        return self.cfg, self.ir

    # ----------------------------------------------------------------------------------------------

    def fill_edges_if_need(self):
        """
            Generates edges between nodes on the same level of nesting.
        """
        if len(self.nodes_before) != 0:
            new_nodes = sorted(list(set(self.cfg.Nodes) - set(self.nodes_before)), key=lambda x: x.Id)
            nodes_wo_edge = [node for node in self.nodes_before if len(node.OEdges) == 0]
            if len(new_nodes) != 0:
                target_node = new_nodes[0]
                curr_node = self.ir.CurNode
                for node_wo_edge in nodes_wo_edge:
                    self.ir.set_cur_node(node_wo_edge)
                    oper = self.create_always_true_oper()
                    self.ir.jump(target_node, oper, True)

                self.ir.set_cur_node(curr_node)

        self.nodes_before = list(self.cfg.Nodes)

    # ----------------------------------------------------------------------------------------------

    def create_if_node(self, if_expr):
        """
            Parses if expression and creates start node for this expression.
            Then parses body of if expression.
        Parameters
        ----------
        if_expr
            If expression.
        """
        if get_type(if_expr) != 'If':
            raise Exception('Not an if node.')

        node = self.cfg.new_node()
        self.ir.set_cur_node(node)

        left = self.create_operation_from_binary_expression(if_expr.cond.left)
        right = self.create_operation_from_binary_expression(if_expr.cond.right)
        operation = self.compare_oper[if_expr.cond.op]
        p0 = operation(left, right)

        if_dict = {'True': if_expr.iftrue, 'False': if_expr.iffalse}
        self.process_if(if_dict, node, p0)

    # ----------------------------------------------------------------------------------------------

    def process_if(self, if_dict, n1, p0):
        """
            Recursively parses body of if expression.

        Parameters
        ----------
        if_dict
            Dictionary with body of if expression.
        n1
            Operand standind for condition of if expression.
        p0
            Origin node of if expression.
        """
        for k, v in if_dict.items():
            if get_type(v) == 'Compound' and len(v.block_items) != 0:
                self.ir.set_cur_node(n1)
                n2 = self.cfg.new_node()
                self.ir.jump(n2, p0, True if k == 'True' else False)
                self.process_block_items(v.block_items, n2)
            elif get_type(v) == 'If':
                n2 = self.cfg.new_node()
                self.ir.set_cur_node(n2)

                left = self.create_operation_from_binary_expression(v.cond.left)
                right = self.create_operation_from_binary_expression(v.cond.right)
                operation = self.compare_oper[v.cond.op]
                p1 = operation(left, right)

                if_dict = {'True': v.iftrue, 'False': v.iffalse}
                self.ir.set_cur_node(n1)
                self.ir.jump(n2, p0, True if k == 'True' else False)

                self.ir.set_cur_node(n2)
                self.process_if(if_dict, n2, p1)

    # ----------------------------------------------------------------------------------------------

    def create_operation_from_binary_expression(self, expr):
        """
            Recursively parses binary operations like 'a*b*c+d'

        Parameters
        ----------
        expr
            Binary expression.
        Returns
        -------
        oper
            Operand standing for whole binary expression.
        """
        if get_type(expr) == 'BinaryOp':
            left = self.create_operation_from_binary_expression(expr.left)
            right = self.create_operation_from_binary_expression(expr.right)
            operation = self.math_oper[expr.op]
            return operation(left, right)
        elif get_type(expr) == 'ID':
            return self.add_variable_if_not_ex(expr.name)
        elif get_type(expr) == 'Constant':
            return self.add_constant_if_not_ex(expr.value)
        else:
            raise Exception(f'{get_type(expr)} is not implemented.')

    # ----------------------------------------------------------------------------------------------

    def process_block_items(self, block_items, node):
        """
            Processes if expression body.
            Body can have assignment operators and nested if expressions.

        Parameters
        ----------
        block_items
            Assignments and nested if expressions.
        node
            Node where assignment operation will occur.
        """
        for block_item in block_items:
            if get_type(block_item) == 'Assignment':
                if block_item.op == '=':
                    self.ir.set_cur_node(node)
                    if get_type(block_item.rvalue) == 'Constant':
                        operation = self.create_operation_from_binary_expression(block_item.rvalue)
                        self.ir.store(operation, block_item.lvalue.name)
                    else:
                        math_operation = self.math_oper[block_item.rvalue.op]
                        left = self.create_operation_from_binary_expression(block_item.rvalue.left)
                        right = self.create_operation_from_binary_expression(block_item.rvalue.right)
                        self.ir.store(math_operation(left, right), block_item.lvalue.name)
                    # self.fill_edges_if_need()
                else:
                    raise Exception(f'{block_item.op} is not implemented.')
            elif get_type(block_item) == 'If':
                self.create_if_node(block_item)

    # ----------------------------------------------------------------------------------------------

    def get_variable(self, name='k'):
        self.variable_counter += 1
        return f'{name}{self.variable_counter}'

    # ----------------------------------------------------------------------------------------------

    def add_variable_if_not_ex(self, name):
        if name not in self.variables:
            print(name)
            self.variables[name] = self.ir.load(name)

        return self.variables[name]

    # ----------------------------------------------------------------------------------------------

    def add_constant_if_not_ex(self, value):
        if value not in self.variables:
            self.variables[value] = self.ir.new_constant(value)

        return self.variables[value]

    # ----------------------------------------------------------------------------------------------

    def create_always_true_oper(self):
        zero = self.add_constant_if_not_ex(0)
        one = self.add_constant_if_not_ex(1)
        return self.compare_oper['>'](one, zero)


# ----------------------------------------------------------------------------------------------

def get_type(item):
    return type(item).__name__
