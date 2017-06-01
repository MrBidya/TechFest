import re
from .parser import validate_equation, validate_inequality, extract_var, is_number
from sympy import simplify, Eq, solveset, Symbol
from sympy.solvers import solve
from sympy.logic.boolalg import BooleanTrue, BooleanFalse, Or, And
from sympy.solvers.inequalities import reduce_inequalities
from .exceptions import AnyValueIsASolutionException, NoRealRootsException, InvalidFormatException
from core.algebra.helpers import format_inequality_result_string


class Equation:
    def __init__(self, equation_str):
        # Validate equation_str
        equation_str = validate_equation(equation_str)

        # Check if right side is passed
        split_eq_str = equation_str.split('=')
        if len(split_eq_str) == 2 and split_eq_str[1]:
            left_side = simplify(split_eq_str[0])
            right_side = simplify(split_eq_str[1])
            equation = Eq(left_side - right_side)
            # Set variables
            self.variables = [x[0] for x in set([tuple(left_side.free_symbols), tuple(right_side.free_symbols)]) if x]

        else:
            equation = Eq(simplify(split_eq_str[0], 0))
            self.variables = list(equation.free_symbols)

        self.equation = equation

    def __format_result(self, roots):
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




    def solve(self):
        roots = solve(self.equation)
        result = self.__format_result(roots)
        return result

    def get_eq_vars(self):
        return self.variables


class Inequality(object):
    def __init__(self, inequality_str):
        # Validate inequality str
        inequality_str = validate_inequality(inequality_str)

        # Check if right side is passed
        split_ie_str = re.split('<|>|>=|<=|', inequality_str)

        # Save ie str, because sympy does not have Ie object (analogous to Eq obj)
        if len(split_ie_str) == 1:
            # 'x-1' is invalid inequality
            raise InvalidFormatException()
        elif len(split_ie_str) == 2 and not split_ie_str[1]:
            # make 'x-1<' to 'x-1<0'
            inequality_str = inequality_str + '0'

        self.inequality_str = inequality_str

        # Set inequality variables
        # NOTE that only the first letter is extracted for now
        self.variables = extract_var(self.inequality_str)

    def __format_result(self, result):
        if isinstance(result, Or) or isinstance(result, And):
            result = format_inequality_result_string(result)
        if isinstance(result, BooleanFalse):
            result = []
        elif isinstance(result, BooleanTrue):
            raise AnyValueIsASolutionException()
        return result


    def solve(self):
        result = reduce_inequalities(self.inequality_str)
        result = self.__format_result(result)
        return result

    def get_ie_vars(self):
        return self.variables


