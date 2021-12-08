"""
Test file.
"""

from cfg.graph import Graph
from cfg.node import Node
from cfg.edge import Edge
from cfg.parser import Parser

# ==================================================================================================
def case_001_build_manual():
    # Build CFG manually.
    cfg = Graph()
    node0 = cfg.new_node()
    node0.Opers = []
    node1 = cfg.new_node()
    node1.Opers = [' 1. BEGIN', ' 2. P0 = a > b', ' 3. JUMP P0==T', ' 4. JUMP P0=F', ' 5. END']
    node2 = cfg.new_node()
    node2.Opers = [' 6. BEGIN', ' 7. V0 = a + b', ' 8. R = V0', ' 9. END']
    node3 = cfg.new_node()
    node3.Opers = ['10. BEGIN', '11. V1 = a - b', '12. R = V1', '13. END']
    node4 = cfg.new_node()
    node4.Opers = []
    cfg.add_edge(node0, node1)
    cfg.add_edge(node1, node2)
    cfg.add_edge(node1, node3)
    cfg.add_edge(node2, node4)
    cfg.add_edge(node3, node4)

    # Print.
    cfg.print()

# ==================================================================================================
def case_002_parser_parse():
    parser=Parser()
    parser.parse('cases/001_if.c').print()

if __name__ == '__main__':
    #case_001_build_manual()
    case_002_parser_parse()

# ==================================================================================================
