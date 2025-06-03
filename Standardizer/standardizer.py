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

# Standardizer Node class (different from Parser Node)
class StandardizerNode:
    def __init__(self):
        self.data = None
        self.depth = 0
        self.parent = None
        self.children = []
        self.is_standardized = False

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def get_degree(self):
        return len(self.children)
    
    def get_children(self):
        return self.children

    def set_depth(self, depth):
        self.depth = depth

    def get_depth(self):
        return self.depth

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def standardize(self):
        if not self.is_standardized:
            for child in self.children:
                child.standardize()

            if self.data == "let":
                # Standardize LET node
                temp1 = self.children[0].children[1]
                temp1.set_parent(self)
                temp1.set_depth(self.depth + 1)
                temp2 = self.children[1]
                temp2.set_parent(self.children[0])
                temp2.set_depth(self.depth + 2)
                self.children[1] = temp1
                self.children[0].set_data("lambda")
                self.children[0].children[1] = temp2
                self.set_data("gamma")
                
            elif self.data == "where":
                temp = self.children[0]
                self.children[0] = self.children[1]
                self.children[1] = temp
                self.set_data("let")
                self.standardize()
                
            elif self.data == "function_form":
                Ex = self.children[-1]
                current_lambda = NodeFactory.get_node_with_parent("lambda", self.depth + 1, self, [], True)
                self.children.insert(1, current_lambda)

                i = 2
                while self.children[i] != Ex:
                    V = self.children[i]
                    self.children.pop(i)
                    V.set_depth(current_lambda.depth + 1)
                    V.set_parent(current_lambda)
                    current_lambda.children.append(V)

                    if len(self.children) > 3:
                        current_lambda = NodeFactory.get_node_with_parent("lambda", current_lambda.depth + 1, current_lambda, [], True)
                        current_lambda.get_parent().children.append(current_lambda)

                current_lambda.children.append(Ex)
                self.children.pop(2)
                self.set_data("=")
                
            elif self.data == "lambda":
                if len(self.children) > 2:
                    Ey = self.children[-1]
                    current_lambda = NodeFactory.get_node_with_parent("lambda", self.depth + 1, self, [], True)
                    self.children.insert(1, current_lambda)

                    i = 2
                    while self.children[i] != Ey:
                        V = self.children[i]
                        self.children.pop(i)
                        V.set_depth(current_lambda.depth + 1)
                        V.set_parent(current_lambda)
                        current_lambda.children.append(V)

                        if len(self.children) > 3:
                            current_lambda = NodeFactory.get_node_with_parent("lambda", current_lambda.depth + 1, current_lambda, [], True)
                            current_lambda.get_parent().children.append(current_lambda)

                    current_lambda.children.append(Ey)
                    self.children.pop(2)
                    
            elif self.data == "within":
                X1 = self.children[0].children[0]
                X2 = self.children[1].children[0]
                E1 = self.children[0].children[1]
                E2 = self.children[1].children[1]
                gamma = NodeFactory.get_node_with_parent("gamma", self.depth + 1, self, [], True)
                lambda_ = NodeFactory.get_node_with_parent("lambda", self.depth + 2, gamma, [], True)
                X1.set_depth(X1.get_depth() + 1)
                X1.set_parent(lambda_)
                X2.set_depth(X1.get_depth() - 1)
                X2.set_parent(self)
                E1.set_depth(E1.get_depth())
                E1.set_parent(gamma)
                E2.set_depth(E2.get_depth() + 1)
                E2.set_parent(lambda_)
                lambda_.children.append(X1)
                lambda_.children.append(E2)
                gamma.children.append(lambda_)
                gamma.children.append(E1)
                self.children.clear()
                self.children.append(X2)
                self.children.append(gamma)
                self.set_data("=")
                
            elif self.data == "@":
                gamma1 = NodeFactory.get_node_with_parent("gamma", self.depth + 1, self, [], True)
                e1 = self.children[0]
                e1.set_depth(e1.get_depth() + 1)
                e1.set_parent(gamma1)
                n = self.children[1]
                n.set_depth(n.get_depth() + 1)
                n.set_parent(gamma1)
                gamma1.children.append(n)
                gamma1.children.append(e1)
                self.children.pop(0)
                self.children.pop(0)
                self.children.insert(0, gamma1)
                self.set_data("gamma")
                
            elif self.data == "and":
                comma = NodeFactory.get_node_with_parent(",", self.depth + 1, self, [], True)
                tau = NodeFactory.get_node_with_parent("tau", self.depth + 1, self, [], True)

                for equal in self.children:
                    equal.children[0].set_parent(comma)
                    equal.children[1].set_parent(tau)
                    comma.children.append(equal.children[0])
                    tau.children.append(equal.children[1])

                self.children.clear()
                self.children.append(comma)
                self.children.append(tau)
                self.set_data("=")
                
            elif self.data == "rec":
                X = self.children[0].children[0]
                E = self.children[0].children[1]
                F = NodeFactory.get_node_with_parent(X.get_data(), self.depth + 1, self, X.children, True)
                G = NodeFactory.get_node_with_parent("gamma", self.depth + 1, self, [], True)
                Y = NodeFactory.get_node_with_parent("<Y*>", self.depth + 2, G, [], True)
                L = NodeFactory.get_node_with_parent("lambda", self.depth + 2, G, [], True)

                X.set_depth(L.depth + 1)
                X.set_parent(L)
                E.set_depth(L.depth + 1)
                E.set_parent(L)
                L.children.append(X)
                L.children.append(E)
                G.children.append(Y)
                G.children.append(L)
                self.children.clear()
                self.children.append(F)
                self.children.append(G)
                self.set_data("=")

            self.is_standardized = True

class NodeFactory:
    @staticmethod
    def get_node(data, depth):
        node = StandardizerNode()
        node.set_data(data)
        node.set_depth(depth)
        node.children = []
        return node

    @staticmethod
    def get_node_with_parent(data, depth, parent, children, is_standardized):
        node = StandardizerNode()
        node.set_data(data)
        node.set_depth(depth)
        node.set_parent(parent)
        node.children = children
        node.is_standardized = is_standardized
        return node

class ASTFactory:
    def __init__(self):
        pass

    def get_abstract_syntax_tree(self, data):
        if not data:
            return None
            
        root = NodeFactory.get_node(data[0], 0)
        previous_node = root
        current_depth = 0

        for s in data[1:]:
            i = 0
            d = 0

            while i < len(s) and s[i] == '.':
                d += 1
                i += 1

            current_node = NodeFactory.get_node(s[i:], d)

            if current_depth < d:
                previous_node.children.append(current_node)
                current_node.set_parent(previous_node)
            else:
                while previous_node.get_depth() != d:
                    previous_node = previous_node.get_parent()
                previous_node.get_parent().children.append(current_node)
                current_node.set_parent(previous_node.get_parent())

            previous_node = current_node
            current_depth = d
        return AST(root)

class AST:
    def __init__(self, root=None):
        self.root = root

    def set_root(self, root):
        self.root = root

    def get_root(self):
        return self.root

    def standardize(self):
        if self.root and not self.root.is_standardized:
            self.root.standardize()

    def pre_order_traverse(self, node, i):
        print("." * i + str(node.get_data()))
        for child in node.children:
            self.pre_order_traverse(child, i + 1)

    def print_ast(self):
        if self.root:
            self.pre_order_traverse(self.get_root(), 0)
        else:
            print("AST is empty")