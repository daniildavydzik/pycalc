class Operator:
    def __init__(self, priority, associativity, is_binary,  func):
        self.priority = priority
        self.associativity = associativity
        self.func = func
        self.name = None
        self.const = None
        self.is_binary = is_binary


operators_dict = {
    '>=': Operator(0, 1, True, lambda x, y: x >= y),
    '<=': Operator(0, 1, True, lambda x, y: x <= y),
    '==': Operator(0, 1, True, lambda x, y: x == y),
    '!=': Operator(0, 1, True, lambda x, y: x != y),
    '>': Operator(0, 1, True, lambda x, y: x > y),
    '<': Operator(0, 1, True, lambda x, y: x >= y),
    ',': Operator(1, 1, True, lambda x, y: [x, y]),
    '+': Operator(2, 1, True, lambda x, y: x+y),
    '-': Operator(2, 1,  True, lambda x, y: x-y),
    'const': Operator(2, 1, True, lambda x: x),
    '*': Operator(3, 1, True, lambda x, y: x*y),
    '/': Operator(3, 1, True, lambda x, y: x/y),
    '%': Operator(3, 1, True, lambda x, y: x % y),
    'unary_minus': Operator(4, 1, False, lambda x: -x),
    'unary_plus': Operator(4, 1, False, lambda x: x),
    '^': Operator(5, 2, True, lambda x, y: x**y),
    'func': Operator(6, 1, True, lambda func, args: func(*args) if type(args) is list else func(*[args])),

}
