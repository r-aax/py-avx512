from pycparser import parse_file, c_generator
import os
from cfg.graph import Graph
from cfg.node import Node
from cfg.edge import Edge


class Parser:

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        self.__variable_counter = 0
        self.__start_index = 0
        self.__cfg = Graph()
        self.__start_node = self.__cfg.new_node()
        self.__stop_node = self.__cfg.new_node()
        self.__cfg.StartNode=self.__start_node
        self.__cfg.StopNode=self.__stop_node
        self.__start_node_used = False

    # ----------------------------------------------------------------------------------------------

    def parse(self, path):
        src = os.path.abspath(path)
        ast = parse_file(src)  # , cpp_path='C:\\MinGW\\bin\\cpp.exe',use_cpp=True)
        body = ast.ext[0].body
        i = 0

        for item in body.block_items:
            if type(item).__name__ != 'If':
                raise Exception('Not implemented')

            self.create_if_node(item)

        return  self.__cfg

    # ----------------------------------------------------------------------------------------------

    def create_if_node(self, item):
        if type(item).__name__ != 'If':
            raise Exception('Not an if node.')

        cond = item.cond
        operation = cond.op
        variable = self.get_variable('P')
        node = self.__cfg.new_node()

        if self.__start_node_used is False:
            self.__cfg.add_edge(self.__start_node, node)
            self.__start_node_used = True

        expression = self.get_expression(cond.left.name, operation, cond.right.name)
        node.Opers = [f' {self.__start_index}. BEGIN',
                      f' {self.__start_index + 1}. {variable} = {expression}',
                      f' {self.__start_index + 2}. JUMP {variable} == T',
                      f' {self.__start_index + 3}. JUMP {variable} == F',
                      f' {self.__start_index + 4}. END']

        self.__start_index += 5

        self.create_return_nodes_for_if_item(node, item)

    # ----------------------------------------------------------------------------------------------

    def get_expression(self, left_name, operation, right_name):
        return f'{left_name} {operation} {right_name}'

    # ----------------------------------------------------------------------------------------------

    def create_return_nodes_for_if_item(self, origin_node, if_expression):
        if type(if_expression).__name__ != 'If':
            raise Exception('Not an IF node.')

        for item in if_expression.iffalse.block_items:
            if type(item).__name__ != 'Return':
                continue

            self.create_return_node(item, origin_node)

        for item in if_expression.iftrue.block_items:
            if type(item).__name__ != 'Return':
                continue

            self.create_return_node(item, origin_node)

    # ----------------------------------------------------------------------------------------------

    def create_return_node(self, return_expression, origin_node):
        expr = return_expression.expr
        if type(expr).__name__ != 'BinaryOp':
            raise Exception(f'Not implemented {type(expr).__name__}')

        variable = self.get_variable('V')
        expression = self.get_expression(expr.left.name, expr.op, expr.right.name)
        return_node = self.__cfg.new_node()

        return_node.Opers = [f' {self.__start_index}. BEGIN',
                             f' {self.__start_index + 1}. {variable} = {expression}',
                             f' {self.__start_index + 2}. R = {variable}',
                             f' {self.__start_index + 3}. END']

        self.__start_index += 4

        self.__cfg.add_edge(origin_node, return_node)
        self.__cfg.add_edge(return_node, self.__stop_node)

    # ----------------------------------------------------------------------------------------------

    def get_variable(self, name):
        self.__variable_counter += 1
        return f'{name}{self.__variable_counter}'
