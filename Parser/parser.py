from LexicalAnalyzer.lexical_analyzer import TokenType, Token
from Parser.node import Node, NodeType


class Parser:
    """
    A recursive descent parser for a functional programming language.
    This parser implements a grammar for a functional language that supports:
    - Let expressions with variable bindings
    - Lambda functions (fn expressions)  
    - Conditional expressions (->)
    - Boolean operations (or, &, not)
    - Arithmetic operations (+, -, *, /, **)
    - Comparison operations (gr, ge, ls, le, eq, ne, >, >=, <, <=)
    - Function application (gamma)
    - Tuple construction (tau)
    - Pattern matching and recursion (rec)
    - Where clauses for local definitions
    The parser takes a list of tokens as input and produces an Abstract Syntax Tree (AST)
    represented as a list of Node objects. It follows a predictive parsing approach
    where each grammar rule is implemented as a separate method.
    Attributes:
        tokens (list): List of Token objects to be parsed
        ast (list): Stack-based representation of the AST being constructed
        string_ast (list): String representation of the AST for display purposes
    Methods:
        parse(): Main parsing method that initiates parsing and returns the AST
        convert_ast_to_string_ast(): Converts the internal AST to a readable string format
        E(), Ew(), T(), Ta(), Tc(), B(), Bt(), Bs(), Bp(), A(), At(), Af(), Ap(), R(), Rn(): 
            Grammar rule methods for expressions at different precedence levels
        D(), Da(), Dr(), Db(): Grammar rule methods for declarations and definitions
        Vb(), Vl(): Grammar rule methods for variable bindings and variable lists
        _add_strings(): Helper method for string AST formatting
    The parser uses a bottom-up approach to build the AST, where nodes are pushed onto
    a stack and later combined based on their arity (number of children).
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.ast = []
        self.string_ast = []

    def parse(self):
        self.tokens.append(Token(TokenType.END, "EOF"))
        self.E()
        if self.tokens[0].type == TokenType.END:
            return self.ast
        else:
            print("Parsing Unsuccessful! Remaining tokens:")
            for token in self.tokens:
                print(f"<{token.type}, {token.value}>")
            return None

    def convert_ast_to_string_ast(self):
        dots = ""
        stack = []

        while self.ast:
            if not stack:
                if self.ast[-1].no_of_children == 0:
                    self._add_strings(dots, self.ast.pop())
                else:
                    stack.append(self.ast.pop())
            else:
                if self.ast[-1].no_of_children > 0:
                    stack.append(self.ast.pop())
                    dots += "."
                else:
                    stack.append(self.ast.pop())
                    dots += "."
                    while stack[-1].no_of_children == 0:
                        self._add_strings(dots, stack.pop())
                        if not stack:
                            break
                        dots = dots[:-1]
                        node = stack.pop()
                        node.no_of_children -= 1
                        stack.append(node)

        self.string_ast.reverse()
        return self.string_ast

    def _add_strings(self, dots, node):
        if node.type in [
            NodeType.identifier, NodeType.integer, NodeType.string,
            NodeType.true_value, NodeType.false_value, NodeType.nil, NodeType.dummy
        ]:
            self.string_ast.append(f"{dots}<{node.type.name.upper()}:{node.value}>")
        elif node.type == NodeType.fcn_form:
            self.string_ast.append(f"{dots}function_form")
        else:
            self.string_ast.append(f"{dots}{node.value}")

    def E(self):
        token = self.tokens[0]
        if token.type == TokenType.KEYWORD and token.value == "let":
            self.tokens.pop(0)
            self.D()
            if self.tokens[0].value != "in":
                print("Error: 'in' expected after 'let'")
            self.tokens.pop(0)
            self.E()
            self.ast.append(Node(NodeType.let, "let", 2))
        elif token.type == TokenType.KEYWORD and token.value == "fn":
            self.tokens.pop(0)
            count = 0
            while self.tokens[0].type == TokenType.IDENTIFIER or self.tokens[0].value == "(":
                self.Vb()
                count += 1
            if self.tokens[0].value != ".":
                print("Error: '.' expected after fn parameters")
            self.tokens.pop(0)
            self.E()
            self.ast.append(Node(NodeType.lambda_expr, "lambda", count + 1))
        else:
            self.Ew()

    def Ew(self):
        self.T()
        if self.tokens[0].value == "where":
            self.tokens.pop(0)
            self.Dr()
            self.ast.append(Node(NodeType.where, "where", 2))

    def T(self):
        self.Ta()
        count = 1
        while self.tokens[0].value == ",":
            self.tokens.pop(0)
            self.Ta()
            count += 1
        if count > 1:
            self.ast.append(Node(NodeType.tau, "tau", count))

    def Ta(self):
        self.Tc()
        while self.tokens[0].value == "aug":
            self.tokens.pop(0)
            self.Tc()
            self.ast.append(Node(NodeType.aug, "aug", 2))

    def Tc(self):
        self.B()
        if self.tokens[0].value == "->":
            self.tokens.pop(0)
            self.Tc()
            if self.tokens[0].value != "|":
                print("Error: '|' expected in conditional")
            self.tokens.pop(0)
            self.Tc()
            self.ast.append(Node(NodeType.conditional, "->", 3))

    def B(self):
        self.Bt()
        while self.tokens[0].value == "or":
            self.tokens.pop(0)
            self.Bt()
            self.ast.append(Node(NodeType.op_or, "or", 2))

    def Bt(self):
        self.Bs()
        while self.tokens[0].value == "&":
            self.tokens.pop(0)
            self.Bs()
            self.ast.append(Node(NodeType.op_and, "&", 2))

    def Bs(self):
        if self.tokens[0].value == "not":
            self.tokens.pop(0)
            self.Bp()
            self.ast.append(Node(NodeType.op_not, "not", 1))
        else:
            self.Bp()

    def Bp(self):
        self.A()
        if self.tokens[0].value in ["gr", "ge", "ls", "le", "eq", "ne", ">", ">=", "<", "<="]:
            op = self.tokens.pop(0).value
            self.A()
            mapped_op = {
                ">": "gr", ">=": "ge", "<": "ls", "<=": "le"
            }.get(op, op)
            self.ast.append(Node(NodeType.op_compare, mapped_op, 2))

    def A(self):
        if self.tokens[0].value in {"+", "-"}:
            unary = self.tokens.pop(0).value
            self.At()
            if unary == "-":
                self.ast.append(Node(NodeType.op_neg, "neg", 1))
        else:
            self.At()
        while self.tokens[0].value in {"+", "-"}:
            op = self.tokens.pop(0).value
            self.At()
            node_type = NodeType.op_plus if op == "+" else NodeType.op_minus
            self.ast.append(Node(node_type, op, 2))

    def At(self):
        self.Af()
        while self.tokens[0].value in {"*", "/"}:
            op = self.tokens.pop(0).value
            self.Af()
            node_type = NodeType.op_mul if op == "*" else NodeType.op_div
            self.ast.append(Node(node_type, op, 2))

    def Af(self):
        self.Ap()
        if self.tokens[0].value == "**":
            self.tokens.pop(0)
            self.Af()
            self.ast.append(Node(NodeType.op_pow, "**", 2))

    def Ap(self):
        self.R()
        while self.tokens[0].value == "@":
            self.tokens.pop(0)
            if self.tokens[0].type != TokenType.IDENTIFIER:
                print("Error: identifier expected after '@'")
                return
            self.ast.append(Node(NodeType.identifier, self.tokens[0].value, 0))
            self.tokens.pop(0)
            self.R()
            self.ast.append(Node(NodeType.at, "@", 3))

    def R(self):
        self.Rn()
        while self.tokens[0].type in [TokenType.IDENTIFIER, TokenType.INTEGER, TokenType.STRING] or \
              self.tokens[0].value in ["true", "false", "nil", "dummy", "("]:
            self.Rn()
            self.ast.append(Node(NodeType.gamma, "gamma", 2))

    def Rn(self):
        token = self.tokens[0]
        if token.type == TokenType.IDENTIFIER:
            self.ast.append(Node(NodeType.identifier, token.value, 0))
        elif token.type == TokenType.INTEGER:
            self.ast.append(Node(NodeType.integer, token.value, 0))
        elif token.type == TokenType.STRING:
            self.ast.append(Node(NodeType.string, token.value, 0))
        elif token.type == TokenType.KEYWORD:
            keyword_map = {
                "true": NodeType.true_value,
                "false": NodeType.false_value,
                "nil": NodeType.nil,
                "dummy": NodeType.dummy,
            }
            if token.value in keyword_map:
                self.ast.append(Node(keyword_map[token.value], token.value, 0))
            else:
                print(f"Unexpected keyword in Rn: {token.value}")
        elif token.value == "(":
            self.tokens.pop(0)
            self.E()
            if self.tokens[0].value != ")":
                print("Error: ')' expected")
            else:
                self.tokens.pop(0)
            return
        else:
            print(f"Unexpected token in Rn: {token}")
        self.tokens.pop(0)


    def D(self):
        self.Da()
        if self.tokens[0].value == "within":
            self.tokens.pop(0)
            self.D()
            self.ast.append(Node(NodeType.within, "within", 2))

    def Da(self):
        self.Dr()
        n = 1
        while self.tokens[0].value == "and":
            self.tokens.pop(0)
            self.Dr()
            n += 1
        if n > 1:
            self.ast.append(Node(NodeType.and_op, "and", n))

    def Dr(self):
        is_rec = False
        if self.tokens[0].value == "rec":
            self.tokens.pop(0)
            is_rec = True
        self.Db()
        if is_rec:
            self.ast.append(Node(NodeType.rec, "rec", 1))

    def Db(self):
        if self.tokens[0].type == TokenType.PUNCTUATION and self.tokens[0].value == "(":
            self.tokens.pop(0)
            self.D()
            if self.tokens[0].value != ")":
                print("Parsing error at Db #1")
            self.tokens.pop(0)
        elif self.tokens[0].type == TokenType.IDENTIFIER:
            if self.tokens[1].value == "(" or self.tokens[1].type == TokenType.IDENTIFIER:
                self.ast.append(Node(NodeType.identifier, self.tokens[0].value, 0))
                self.tokens.pop(0)
                n = 1
                while self.tokens[0].type == TokenType.IDENTIFIER or self.tokens[0].value == "(":
                    self.Vb()
                    n += 1
                if self.tokens[0].value != "=":
                    print("Parsing error at Db #2")
                self.tokens.pop(0)
                self.E()
                self.ast.append(Node(NodeType.fcn_form, "fcn_form", n + 1))
            elif self.tokens[1].value == "=":
                self.ast.append(Node(NodeType.identifier, self.tokens[0].value, 0))
                self.tokens.pop(0)
                self.tokens.pop(0)
                self.E()
                self.ast.append(Node(NodeType.equal, "=", 2))
            elif self.tokens[1].value == ",":
                self.Vl()
                if self.tokens[0].value != "=":
                    print("Parsing error at Db")
                self.tokens.pop(0)
                self.E()
                self.ast.append(Node(NodeType.equal, "=", 2))

    def Vb(self):
        if self.tokens[0].type == TokenType.PUNCTUATION and self.tokens[0].value == "(":
            self.tokens.pop(0)
            isVl = False
            if self.tokens[0].type == TokenType.IDENTIFIER:
                self.Vl()
                isVl = True
            if self.tokens[0].value != ")":
                print("Parse error unmatch )")
            self.tokens.pop(0)
            if not isVl:
                self.ast.append(Node(NodeType.empty_params, "()", 0))
        elif self.tokens[0].type == TokenType.IDENTIFIER:
            self.ast.append(Node(NodeType.identifier, self.tokens[0].value, 0))
            self.tokens.pop(0)

    def Vl(self):
        n = 0
        while True:
            if n > 0:
                self.tokens.pop(0)
            if not self.tokens[0].type == TokenType.IDENTIFIER:
                print("Parse error: an identifier was expected")
            self.ast.append(Node(NodeType.identifier, self.tokens[0].value, 0))
            self.tokens.pop(0)
            n += 1
            if self.tokens[0].value != ",":
                break
        if n > 1:
            self.ast.append(Node(NodeType.comma, ",", n))
