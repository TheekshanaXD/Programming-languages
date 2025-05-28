from enum import Enum, auto

class NodeType(Enum):
    let = auto()
    fcn_form = auto()
    identifier = auto()
    integer = auto()
    string = auto()
    where = auto()
    gamma = auto()
    lambda_expr = auto()
    tau = auto()
    rec = auto()
    aug = auto()
    conditional = auto()
    op_or = auto()
    op_and = auto()
    op_not = auto()
    op_compare = auto()
    op_plus = auto()
    op_minus = auto()
    op_neg = auto()
    op_mul = auto()
    op_div = auto()
    op_pow = auto()
    at = auto()
    true_value = auto()
    false_value = auto()
    nil = auto()
    dummy = auto()
    within = auto()
    and_op = auto()
    equal = auto()
    comma = auto()
    empty_params = auto()

class Node:
    def __init__(self, node_type, value, no_of_children):
        self.type = node_type
        self.value = value
        self.no_of_children = no_of_children
