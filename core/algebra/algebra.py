import re
from .parser import validate_equation
from sympy import simplify, Eq, solveset, Symbol
from sympy.solvers import solve


class Equation(object):
    def __init__(self, equation_str):
        # Validate equation_str
        equation_str = validate_equation(equation_str)

        # Check if right side is passed
        split_eq_str = equation_str.split('=')
        if len(split_eq_str) == 2 and is_number(split_eq_str[1]):
            equation = Eq(simplify(split_eq_str[0]), simplify(split_eq_str[1]))
        else: #len(split_eq_str) == 1:
            equation = Eq(simplify(split_eq_str[0], 0))

        self.equation = equation

    def solve(self):
        roots = solve(self.equation)
        results = []
        # Get real roots only
        for root in roots:
            if not root.is_imaginary:
                results.append(root)
        return results


    def get_eq_var(self):
        # Assumes only 1 variable is used in equation
        eq_var = str(list(self.equation.free_symbols)[0])
        return eq_var


class Inequality(object):
    def __init__(self, inequality_str):
        # Validate equation_str
        inequality_str = validate_inequality(inequality_str)

        # Check if right side is passed
        split_ie_str = re.split('<|>|>=|<=')

        if len(split_ie_str) == 2 and is_number(split_ie_str[1]):
            inequality = Eq(simplify(split_ie_str[0]), simplify(split_ie_str[1]))
        else:
            inequality = Eq(simplify(split_eq_str[0], 0))

        self.inequality = inequality


def extract_var(input_str):
    for letter in [chr(x) for x in range(97, 123)]:
        # lower lowers all letters
        if letter in input_str.lower():
            return letter
    raise ValueError('Cannot parse equation variable')


def is_number(input_str):
    try:
        input_str = int(input_str)
        return True
    except:
        return False
