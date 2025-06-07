#Create CSE machine to flatten the ST and simulate execution
# -------------------NODES --------------------
class Symbol:
    def __init__(self, data):
        self.data = data

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

class Rand(Symbol):
    def __init__(self, data):
        super().__init__(data)

class Rator(Symbol):
    def __init__(self, data):
        super().__init__(data)

class B(Symbol):
    def __init__(self):
        super().__init__("b")
        self.symbols = []

class Beta(Symbol):
    def __init__(self):
        super().__init__("beta")

class Bool(Rand):
    def __init__(self, data):
        super().__init__(data)

class Bop(Rator):
    def __init__(self, data):
        super().__init__(data)

class Uop(Rator):
    def __init__(self, data):
        super().__init__(data)

class Delta(Symbol):
    def __init__(self, i):
        super().__init__("delta")
        self.index = i
        self.symbols = []

    def set_index(self, i):
        self.index = i

    def get_index(self):
        return self.index

class Dummy(Rand):
    def __init__(self):
        super().__init__("dummy")

class E(Symbol):
    def __init__(self, i):
        super().__init__("e")
        self.index = i
        self.parent = None
        self.is_removed = False
        self.values = {}

    def set_parent(self, e):
        self.parent = e

    def get_parent(self):
        return self.parent

    def set_index(self, i):
        self.index = i

    def get_index(self):
        return self.index

    def set_is_removed(self, is_removed):
        self.is_removed = is_removed

    def get_is_removed(self):
        return self.is_removed

    def lookup(self, id):
        for key in self.values:
            if key.get_data() == id.get_data():
                return self.values[key]
        if self.parent is not None:
            return self.parent.lookup(id)
        else:
            return Symbol(id.get_data())

class Err(Symbol):
    def __init__(self):
        super().__init__("")

class Eta(Symbol):
    def __init__(self):
        super().__init__("eta")
        self.index = None
        self.environment = None
        self.identifier = None
        self.lambda_ = None

    def set_index(self, i):
        self.index = i

    def get_index(self):
        return self.index

    def set_environment(self, e):
        self.environment = e

    def get_environment(self):
        return self.environment

    def set_identifier(self, identifier):
        self.identifier = identifier

    def set_lambda(self, lambda_):
        self.lambda_ = lambda_

    def get_lambda(self):
        return self.lambda_

class Gamma(Symbol):
    def __init__(self):
        super().__init__("gamma")

class Id(Rand):
    def __init__(self, data):
        super().__init__(data)

class Int(Rand):
    def __init__(self, data):
        super().__init__(data)

class Str(Rand):
    def __init__(self, data):
        super().__init__(data)

class Lambda(Symbol):
    def __init__(self, i):
        super().__init__("lambda")
        self.index = i
        self.environment = None
        self.identifiers = []
        self.delta = None

    def set_environment(self, n):
        self.environment = n

    def get_environment(self):
        return self.environment

    def set_delta(self, delta):
        self.delta = delta

    def get_delta(self):
        return self.delta

    def get_index(self):
        return self.index

class Tau(Symbol):
    def __init__(self, n):
        super().__init__("tau")
        self.n = n

    def get_n(self):
        return self.n

class Tup(Rand):
    def __init__(self):
        super().__init__("tuple")
        self.symbols = []

class Ystar(Symbol):
    def __init__(self):
        super().__init__("<Y*>")

# -------------------- CSEMachine --------------------
class CSEMachine:
    def __init__(self, control, stack, environment):
        self.control = control
        self.stack = stack
        self.environment = environment

    def execute(self):
        current_environment = self.environment[0]
        j = 1
        while self.control:
            current_symbol = self.control.pop()
            if isinstance(current_symbol, Id):
                self.stack.insert(0, current_environment.lookup(current_symbol))
            elif isinstance(current_symbol, Lambda):
                current_symbol.set_environment(current_environment.get_index())
                self.stack.insert(0, current_symbol)
            elif isinstance(current_symbol, Gamma):
                next_symbol = self.stack.pop(0)
                if isinstance(next_symbol, Lambda):
                    lambda_expr = next_symbol
                    e = E(j)
                    j += 1
                    if len(lambda_expr.identifiers) == 1:
                        e.values[lambda_expr.identifiers[0]] = self.stack.pop(0)
                    else:
                        tup = self.stack.pop(0)
                        for i, id in enumerate(lambda_expr.identifiers):
                            e.values[id] = tup.symbols[i]
                    for env in self.environment:
                        if env.get_index() == lambda_expr.get_environment():
                            e.set_parent(env)
                    current_environment = e
                    self.control.append(e)
                    self.control.append(lambda_expr.get_delta())
                    self.stack.insert(0, e)
                    self.environment.append(e)
                elif isinstance(next_symbol, Tup):
                    i = int(self.stack.pop(0).get_data())
                    self.stack.insert(0, next_symbol.symbols[i - 1])
                elif isinstance(next_symbol, Ystar):
                    lambda_expr = self.stack.pop(0)
                    eta = Eta()
                    eta.set_index(lambda_expr.get_index())
                    eta.set_environment(lambda_expr.get_environment())
                    eta.set_identifier(lambda_expr.identifiers[0])
                    eta.set_lambda(lambda_expr)
                    self.stack.insert(0, eta)
                elif isinstance(next_symbol, Eta):
                    lambda_expr = next_symbol.get_lambda()
                    self.control.append(Gamma())
                    self.control.append(Gamma())
                    self.stack.insert(0, next_symbol)
                    self.stack.insert(0, lambda_expr)
                else:
                    # Built-in function support (partial)
                    fname = next_symbol.get_data()
                    if fname == "Stem":
                        s = self.stack.pop(0)
                        s.set_data(s.get_data()[0])
                        self.stack.insert(0, s)
                    elif fname == "Stern":
                        s = self.stack.pop(0)
                        s.set_data(s.get_data()[1:])
                        self.stack.insert(0, s)
                    elif fname == "Conc":
                        s1 = self.stack.pop(0)
                        s2 = self.stack.pop(0)
                        s1.set_data(s1.get_data() + s2.get_data())
                        self.stack.insert(0, s1)
                    elif fname == "Order":
                        tup = self.stack.pop(0)
                        self.stack.insert(0, Int(str(len(tup.symbols))))
                    elif fname == "Isinteger":
                        self.stack.insert(0, Bool("true" if isinstance(self.stack[0], Int) else "false"))
                        self.stack.pop(1)
                    elif fname == "Isstring":
                        self.stack.insert(0, Bool("true" if isinstance(self.stack[0], Str) else "false"))
                        self.stack.pop(1)
                    elif fname == "Istuple":
                        self.stack.insert(0, Bool("true" if isinstance(self.stack[0], Tup) else "false"))
                        self.stack.pop(1)
                    elif fname == "Isdummy":
                        self.stack.insert(0, Bool("true" if isinstance(self.stack[0], Dummy) else "false"))
                        self.stack.pop(1)
                    elif fname == "Istruthvalue":
                        self.stack.insert(0, Bool("true" if isinstance(self.stack[0], Bool) else "false"))
                        self.stack.pop(1)
                    elif fname == "Isfunction":
                        self.stack.insert(0, Bool("true" if isinstance(self.stack[0], Lambda) else "false"))
                        self.stack.pop(1)
            elif isinstance(current_symbol, E):
                self.stack.pop(1)
                self.environment[current_symbol.get_index()].set_is_removed(True)
                for env in reversed(self.environment):
                    if not env.get_is_removed():
                        current_environment = env
                        break
            elif isinstance(current_symbol, Rator):
                if isinstance(current_symbol, Uop):
                    rand = self.stack.pop(0)
                    self.stack.insert(0, self.apply_unary_operation(current_symbol, rand))
                elif isinstance(current_symbol, Bop):
                    rand1 = self.stack.pop(0)
                    rand2 = self.stack.pop(0)
                    self.stack.insert(0, self.apply_binary_operation(current_symbol, rand1, rand2))
            elif isinstance(current_symbol, Beta):
                if self.stack[0].get_data() == "true":
                    self.control.pop()
                else:
                    self.control.pop(-2)
                self.stack.pop(0)
            elif isinstance(current_symbol, Tau):
                tup = Tup()
                for _ in range(current_symbol.get_n()):
                    tup.symbols.append(self.stack.pop(0))
                self.stack.insert(0, tup)
            elif isinstance(current_symbol, Delta):
                self.control.extend(current_symbol.symbols)
            elif isinstance(current_symbol, B):
                self.control.extend(current_symbol.symbols)
            else:
                self.stack.insert(0, current_symbol)

    def apply_unary_operation(self, rator, rand):
        if rator.get_data() == "neg":
            return Int(str(-int(rand.get_data())))
        elif rator.get_data() == "not":
            val = rand.get_data() == "true"
            return Bool(str(not val).lower())
        return Err()

    def apply_binary_operation(self, rator, rand1, rand2):
        op = rator.get_data()
        val1 = rand1.get_data()
        val2 = rand2.get_data()
        if op == "+":
            return Int(str(int(val1) + int(val2)))
        elif op == "-":
            return Int(str(int(val1) - int(val2)))
        elif op == "*":
            return Int(str(int(val1) * int(val2)))
        elif op == "/":
            return Int(str(int(int(val1) / int(val2))))
        elif op == "**":
            return Int(str(int(val1) ** int(val2)))
        elif op == "&":
            return Bool(str((val1 == "true") and (val2 == "true")).lower())
        elif op == "or":
            return Bool(str((val1 == "true") or (val2 == "true")).lower())
        elif op == "eq":
            return Bool(str(val1 == val2).lower())
        elif op == "ne":
            return Bool(str(val1 != val2).lower())
        elif op == "ls":
            return Bool(str(int(val1) < int(val2)).lower())
        elif op == "le":
            return Bool(str(int(val1) <= int(val2)).lower())
        elif op == "gr":
            return Bool(str(int(val1) > int(val2)).lower())
        elif op == "ge":
            return Bool(str(int(val1) >= int(val2)).lower())
        elif op == "aug":
            if isinstance(rand2, Tup):
                rand1.symbols.extend(rand2.symbols)
            else:
                rand1.symbols.append(rand2)
            return rand1
        return Err()

    def get_tuple_value(self, tup):
        return "(" + ", ".join(
            self.get_tuple_value(sym) if isinstance(sym, Tup) else sym.get_data()
            for sym in tup.symbols
        ) + ")"

    def get_answer(self):
        self.execute()
        if isinstance(self.stack[0], Tup):
            return self.get_tuple_value(self.stack[0])
        return self.stack[0].get_data()

# -------------------- CSEMachineFactory --------------------
class CSEMachineFactory:
    def __init__(self):
        self.e0 = E(0)
        self.i = 1
        self.j = 0

    def get_symbol(self, node):
        data = node.get_data()
        if data in ("not", "neg"):
            return Uop(data)
        elif data in ("+", "-", "**", "/", "*", "&", "or", "eq", "ne", "ls", "le", "gr", "ge", "aug"):
            return Bop(data)
        elif data == "gamma":
            return Gamma()
        elif data == "tau":
            return Tau(len(node.get_children()))
        elif data == "<Y*>":
            return Ystar()
        elif data.startswith("<IDENTIFIER:"):
            return Id(data[12:-1])
        elif data.startswith("<INTEGER:"):
            return Int(data[9:-1])
        elif data.startswith("<STRING:"):
            return Str(data[9:-2])
        elif data.startswith("<NIL"):
            return Tup()
        elif data.startswith("<TRUE_VALUE:t"):
            return Bool("true")
        elif data.startswith("<TRUE_VALUE:f"):
            return Bool("false")
        elif data.startswith("<dummy>"):
            return Dummy()
        else:
            print("Err node:", data)
            return Err()

    def get_b(self, node):
        b = B()
        b.symbols = self.get_pre_order_traverse(node)
        return b

    def get_lambda(self, node):
        lambda_expr = Lambda(self.i)
        self.i += 1
        lambda_expr.set_delta(self.get_delta(node.get_children()[1]))
        if node.get_children()[0].get_data() == ",":
            for identifier in node.get_children()[0].get_children():
                lambda_expr.identifiers.append(Id(identifier.get_data()[12:-1]))
        else:
            lambda_expr.identifiers.append(Id(node.get_children()[0].get_data()[12:-1]))
        return lambda_expr

    def get_pre_order_traverse(self, node):
        symbols = []
        if node.get_data() == "lambda":
            symbols.append(self.get_lambda(node))
        elif node.get_data() == "->":
            symbols.append(self.get_delta(node.get_children()[1]))
            symbols.append(self.get_delta(node.get_children()[2]))
            symbols.append(Beta())
            symbols.append(self.get_b(node.get_children()[0]))
        else:
            symbols.append(self.get_symbol(node))
            for child in node.get_children():
                symbols.extend(self.get_pre_order_traverse(child))
        return symbols

    def get_delta(self, node):
        delta = Delta(self.j)
        self.j += 1
        delta.symbols = self.get_pre_order_traverse(node)
        return delta

    def get_control(self, ast):
        return [self.e0, self.get_delta(ast.get_root())]

    def get_stack(self):
        return [self.e0]

    def get_environment(self):
        return [self.e0]

    def get_cse_machine(self, ast):
        return CSEMachine(self.get_control(ast), self.get_stack(), self.get_environment())