from pycparser import parse_file, c_generator
import os
import sem
from pycparser.c_ast import ID


class Parser:

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        self.variable_counter = 0
        self.ir = None
        self.cfg = None
        self.out_params_names = None
        self.in_params_names = None
        self.in_params = None
        self.out_params = None
        self.registers = None
        self.constants = None
        self.nodes_before = None
        self.math_oper = None
        self.logical_oper = None
        self.func_call = None
        self.unary = None

    # ----------------------------------------------------------------------------------------------
    def initialize(self):
        self.ir = sem.IR()
        self.cfg = self.ir.CFG
        self.out_params_names = []
        self.in_params_names = []
        self.in_params = dict()
        self.out_params = dict()
        self.registers = dict()
        self.constants = dict()
        self.nodes_before = []
        self.math_oper = {
            '+': self.ir.add,
            '-': self.ir.sub,
            '*': self.ir.mul,
            '/': self.ir.div
        }
        self.logical_oper = {
            '>': self.ir.cmpge,
            '<': self.ir.cmplt,
            '<=': self.ir.cmplte,
            '>=': self.ir.cmpge,
            '==': self.ir.eq,
            '&&': self.ir.l_and,
        }
        self.func_call = {
            'pow': self.ir.pow,
            'sqrt': self.ir.sqrt,
        }
        self.unary = {
            '-': 'unary_minus',
        }

    # ----------------------------------------------------------------------------------------------

    def parse(self, path):
        self.initialize()

        src = os.path.abspath(path)
        ast = parse_file(src)  # , cpp_path='C:\\MinGW\\bin\\cpp.exe',use_cpp=True)
        body = ast.ext[0].body
        self.in_params_names = [k.name for k in ast.ext[0].decl.type.args.params if get_type(k.type) == 'TypeDecl']
        self.out_params_names = [k.name for k in ast.ext[0].decl.type.args.params if get_type(k.type) == 'PtrDecl']
        self.ir.set_in_out_params(self.in_params_names, self.out_params_names)

        for k in self.ir.OutParams:
            self.out_params[k.Id] = k

        node = self.cfg.new_node()
        self.ir.set_cur_node(node)
        self.nodes_before.append(node)
        for k in self.ir.InParams:
            self.in_params[k.Id] = self.ir.load(k.Id)

        for item in body.block_items:
            n = get_type(item)
            if n == 'Decl':  # variable declaration
                self.add_register_if_not_ex(item.name)
                if item.init is not None:
                    self.process_assignment(ID(item.name), item.init, '=')
            elif n == 'Assignment':
                self.process_assignment(item.lvalue, item.rvalue, item.op, None)
            elif n == 'If':
                self.create_if_node(item)
            else:
                raise Exception(f'Block item {n} is not implemented')

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
                    self.jump(node_wo_edge, target_node)

                self.ir.set_cur_node(curr_node)

        self.nodes_before = list(self.cfg.Nodes)

    # ----------------------------------------------------------------------------------------------

    def jump(self, node_wo_edge, target_node):
        self.ir.set_cur_node(node_wo_edge)
        oper = self.create_always_true_oper()
        self.ir.jump(target_node, oper, True)

    # ----------------------------------------------------------------------------------------------

    def mov(self, from_reg, to_reg):
        self.ir.new_oper('mov', args=[from_reg, to_reg])

    # ----------------------------------------------------------------------------------------------

    def create_if_node(self, if_expr, node=None):
        """
            Parses if expression and creates start node for this expression.
            Then parses body of if expression.
        Parameters
        ----------
        node
        if_expr
            If expression.
        """
        if get_type(if_expr) != 'If':
            raise Exception('Not an if node.')

        if node is None:
            node = self.cfg.new_node()

        self.ir.set_cur_node(node)

        left = self.process_binary_expression(if_expr.cond.left)
        right = self.process_binary_expression(if_expr.cond.right)
        operation = self.logical_oper[if_expr.cond.op]
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
        # self.fill_edges_if_need()

        for k, v in if_dict.items():
            if get_type(v) == 'Compound' and len(v.block_items) != 0:
                self.ir.set_cur_node(n1)
                n2 = self.cfg.new_node()
                self.ir.jump(n2, p0, True if k == 'True' else False)
                self.process_block_items(v.block_items, n2)
            elif get_type(v) == 'If':
                n2 = self.cfg.new_node()
                self.ir.set_cur_node(n2)

                left = self.process_binary_expression(v.cond.left)
                right = self.process_binary_expression(v.cond.right)
                operation = self.logical_oper[v.cond.op]
                p1 = operation(left, right)

                if_dict = {'True': v.iftrue, 'False': v.iffalse}
                self.ir.set_cur_node(n1)
                self.ir.jump(n2, p0, True if k == 'True' else False)

                self.ir.set_cur_node(n2)
                self.process_if(if_dict, n2, p1)
            else:
                raise Exception(f'{get_type(v)} is not implemented.')

    # ----------------------------------------------------------------------------------------------

    def process_binary_expression(self, expr):
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
            left = self.process_binary_expression(expr.left)
            right = self.process_binary_expression(expr.right)
            operation = self.math_oper[expr.op] if expr.op in self.math_oper else self.logical_oper[expr.op]
            return operation(left, right)
        elif get_type(expr) == 'ID':
            return self.get_param_or_register(expr.name)
        elif get_type(expr) == 'Constant':
            return self.add_constant_if_not_ex(expr.value)
        elif get_type(expr) == 'FuncCall':
            return self.process_func_call(expr)
        elif get_type(expr) == 'TernaryOp':
            register = self.ir.new_reg()
            newnodes = self.process_ternary_op(expr, register, 'no register name', self.ir.CurNode)
            node = self.cfg.new_node()
            for n in newnodes.values():
                self.jump(n, node)

            self.ir.set_cur_node(node)
            return register

        elif get_type(expr) == 'UnaryOp':
            op = self.process_binary_expression(expr.expr)
            register = self.ir.new_reg()
            self.ir.new_oper(self.unary[expr.op], [op], register)
            return register
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
                self.process_assignment(block_item.lvalue, block_item.rvalue, block_item.op, node)
            elif get_type(block_item) == 'If':
                self.create_if_node(block_item, node)
            else:
                raise Exception(f'Block item {get_type(block_item)} is not implemented.')

    # ----------------------------------------------------------------------------------------------

    def process_assignment(self, l_value, r_value, op, node=None):
        if op == '=':
            if node is None:
                node = self.cfg.new_node()

            self.ir.set_cur_node(node)
            right_oper = None
            n = get_type(r_value)
            if n == 'Constant' or n == 'ID':
                right_oper = self.process_binary_expression(r_value)
            elif n == 'BinaryOp':
                math_operation = self.math_oper[r_value.op]
                left = self.process_binary_expression(r_value.left)
                right = self.process_binary_expression(r_value.right)
                right_oper = math_operation(left, right)
            elif n == 'TernaryOp':
                register_to_store = self.get_param_or_register(l_value.name)
                return self.process_ternary_op(r_value, register_to_store, l_value.name, node)

                return

            elif n == 'FuncCall':
                right_oper = self.process_func_call(r_value)
            else:
                raise Exception(f'Rvalue {get_type(r_value)} is not implemented. - {r_value}')

            left_oper = self.get_param_or_register(l_value.name)
            self.store_or_mov(right_oper, left_oper, l_value.name)

            # self.fill_edges_if_need()
        else:
            raise Exception(f'Operation {op} is not implemented.')

    # ----------------------------------------------------------------------------------------------

    def store_or_mov(self, from_arg, to_arg, to_name):
        if self.is_out_param(to_name):
            self.ir.store(from_arg, to_arg)
        else:
            self.mov(from_arg, to_arg)

    # ----------------------------------------------------------------------------------------------

    def process_ternary_op(self, ternar, register_to_store, register_name, node):
        left = self.process_binary_expression(ternar.cond.left)
        right = self.process_binary_expression(ternar.cond.right)
        right_oper = self.logical_oper[ternar.cond.op](left, right)
        iftrue = self.cfg.new_node()
        iffalse = self.cfg.new_node()
        if_list = [['True', ternar.iftrue, iftrue], ['False', ternar.iffalse, iffalse]]
        for k in if_list:
            self.ir.jump(k[2], right_oper, k[0] == 'True')
            value = self.process_binary_expression(k[1])
            self.ir.set_cur_node(k[2])
            self.store_or_mov(value, register_to_store, register_name)
            self.ir.set_cur_node(node)

        return {'True': iftrue, 'False': iffalse}

    # ----------------------------------------------------------------------------------------------

    def process_func_call(self, func):
        if get_type(func) != 'FuncCall':
            raise Exception(f'Got {get_type(func)}, expected FuncCall.')

        args = [self.process_binary_expression(op) for op in func.args]
        reg = self.ir.new_reg()
        self.ir.new_oper(func.name.name, args=args, res=reg)
        return reg

    # ----------------------------------------------------------------------------------------------

    def is_out_param(self, name):
        return name in self.out_params_names

    # ----------------------------------------------------------------------------------------------

    def is_in_param(self, name):
        return name in self.in_params_names

    # ----------------------------------------------------------------------------------------------

    def get_param_or_register(self, name):
        if self.is_in_param(name):
            return self.load_in_param(name)
        elif self.is_out_param(name):
            return self.out_params[name]
        else:
            return self.get_register(name)

    # ----------------------------------------------------------------------------------------------

    def load_in_param(self, name):
        if name not in self.in_params:
            self.in_params[name] = self.ir.load(name)

        return self.in_params[name]

    # ----------------------------------------------------------------------------------------------

    def get_register(self, name):
        if name not in self.registers:
            raise KeyError(f'{name} is not found in registers.')

        return self.registers[name]

    # ----------------------------------------------------------------------------------------------

    def add_register_if_not_ex(self, name):
        if name not in self.registers:
            self.registers[name] = self.ir.new_reg()

        return self.registers[name]

    # ----------------------------------------------------------------------------------------------

    def add_constant_if_not_ex(self, value):
        if value not in self.constants:
            self.constants[value] = self.ir.new_constant(value)

        return self.constants[value]

    # ----------------------------------------------------------------------------------------------

    def create_always_true_oper(self):
        zero = self.add_constant_if_not_ex(0)
        one = self.add_constant_if_not_ex(1)
        return self.logical_oper['>'](one, zero)


# ----------------------------------------------------------------------------------------------

def get_type(item):
    return type(item).__name__
