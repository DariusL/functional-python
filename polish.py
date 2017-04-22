from enum import Enum


def evaluate(string):
    return _evaluate(tokenize(string))[0].value


def _evaluate(tokens):
    if len(tokens) == 0:
        return tuple()
    if isinstance(tokens[0], Operand):
        return (tokens[0],) + _evaluate(tokens[1:])
    if isinstance(tokens[0], Operator):
        operator = tokens[0]
        stack = _evaluate(tokens[1:])
        left, right, tail = stack[0], stack[1], stack[2:]
        return (Operand(do_operation(operator.value, left.value, right.value)),) + tail


def tokenize(string):
    return [tokenize_single(t) for t in string.split()]


def tokenize_single(string):
    if unicode(string).isnumeric():
        return Operand(int(string))
    return Operator(string)


class Operand:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Operand) and other.value == self.value

    def __repr__(self):
        return str(self.value)


class Operator(Enum):
    add = "+"
    subtract = "-"
    multiply = "*"
    divide = "/"

    def __repr__(self):
        return self.value


def do_operation(operator, left, right):
    # :D
    return eval("{0} {1} {2}".format(left, operator, right))

