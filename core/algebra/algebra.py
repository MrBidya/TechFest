import re
from .parser import validate_equation, validate_inequality
from sympy import simplify, Eq, solveset, Symbol
from sympy.solvers import solve
from sympy.logic.boolalg import BooleanTrue, BooleanFalse
from .exceptions import AnyValueIsASolutionException, NoRealRootsException


class Equation(object):
    def __init__(self, equation_str):
        # Validate equation_str
        equation_str = validate_equation(equation_str)

        # Check if right side is passed
        split_eq_str = equation_str.split('=')
        if len(split_eq_str) == 2:
            left_side = simplify(split_eq_str[0])
            right_side = simplify(split_eq_str[1])
            equation = Eq(left_side - right_side)
            # Set variables
            self.variables = [x[0] for x in set([tuple(left_side.free_symbols), tuple(right_side.free_symbols)]) if x]

        else:
            equation = Eq(simplify(split_eq_str[0], 0))
            self.variables = list(equation.free_symbols)

        self.equation = equation

    def solve(self):
        roots = solve(self.equation)
        results = []
        # Check if roots make sense
        if isinstance(roots, BooleanTrue) or isinstance(roots, BooleanFalse):
            if roots:
                raise AnyValueIsASolutionException()
            else:
                raise NoRealRootsException()
        elif any(type(x) is dict for x in roots):
            results = str(roots)
        else:
            # Get real roots only
            for root in roots:
                if not root.is_imaginary:
                    results.append(root)
            if not results:
                raise NoRealRootsException()
        return results


    def get_eq_vars(self):
        return self.variables


class Inequality(object):
    def __init__(self, inequality_str):
        # Validate equation_str
        inequality_str = validate_inequality(inequality_str)

        # Check if right side is passed
        split_ie_str = re.split('<|>|>=|<=|', inequality_str)

        if len(split_ie_str) == 2 and is_number(split_ie_str[1]):
            inequality = Eq(simplify(split_ie_str[0]), simplify(split_ie_str[1]))
        else:
            inequality = Eq(simplify(split_eq_str[0], 0))

        self.inequality = inequality

    def solve(self):
        import ipdb; ipdb.set_trace() # BREAKPOINT
        pass


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
