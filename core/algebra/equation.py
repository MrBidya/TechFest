import math
import re
import sympy
import sys
from .equation_helpers import get_eq_power, extract_var, get_quad_coeffs, prepare_input
from .meta import AlgebraMeta
from .exceptions import EquationPowerNotSupportedException


class Equation:
    def __repr__(self):
        return self.string

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def from_str(input_str):
        # Can be made more generic using metaclass and inserting power
        # to each subclass but for now powers 2 and 4 are enough
        input_str = input_str.replace(' ','')
        powers_to_eq_types = {
                                1 : LinearEquation,
                                2 : QuadraticEquation,
                                4  : BiquadraticEquation
                              }
        eq_power = get_eq_power(input_str)
        if eq_power not in powers_to_eq_types:
            raise EquationPowerNotSupportedException('Got equation from {} power which is not supported!'.format(eq_power))
        # Prepare input_str for specific equation type
        eq_type = powers_to_eq_types[eq_power]
        input_str = prepare_input(input_str, eq_type)

        return eq_type.from_str(input_str)

class LinearEquation(Equation):
    pass


class QuadraticEquation(Equation):
    def __init__(self, a=1, b=1, c=1, var='x',power=2, res1=None, res2=None, string=None):
        self.SQRT_SIGN = '√'
        self.INVALID_QUADRATIC_EQUATION = 'Invalid quadratic equation!'

        self.a = a
        self.b = b
        self.c = c
        self.var = var
        self.res1 = res1
        self.res2 = res2
        self.power = power
        if string is not None:
            self.string = string
        else:
            self.string = '{}*{}^2 {}*{} {}'.format(self.a, self.var, self.b, self.var, self.c)

    @staticmethod
    def from_str(input_str):
        var = extract_var(input_str)
        coefs = re.findall(r'-?[0-9]+', input_str)
        if len(coefs) != 4:
            # If here, then prepare_input method has failed. Raise
            raise ValueError('Something went wrong while preparing input_str')

        # Coefs contains the following:
        # index 0 is a
        a = int(coefs[0])
        # index 1 is the power of x which must be always 2
        # index 2 is b
        b = int(coefs[2])
        # index 3 is c
        c = int(coefs[3])
        obj = QuadraticEquation(a=a, b=b, c=c, var=var, string=input_str.replace(' ',''))
        return obj


    def solve(self):
        d = self.b ** 2 - 4 * self.a * self.c
        if d < 0:
            raise ValueError('No real roots')
        self.res1 = (-self.b + sympy.sqrt(d)) / (2 * self.a)
        self.res2 = (-self.b - sympy.sqrt(d)) / (2 * self.a)
        if self.res1 == self.res2:
            return self.res1,

        return self.res1, self.res2


class BiquadraticEquation(QuadraticEquation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.power = 4

    @staticmethod
    def from_str(input_str):
        var = extract_var(input_str)
        coefs = re.findall(r'-?[0-9]+', input_str)
        if len(coefs) != 5:
            # If here, then prepare_input method has failed. Raise
            raise ValueError('Something went wrong while preparing input_str')

        # Coefs contains the following:
        # index 0 is a
        a = int(coefs[0])
        # index 1 is the power of x which must be always 2
        # index 2 is b
        b = int(coefs[2])
        # index 3 is c
        c = int(coefs[4])
        obj = BiquadraticEquation(a=a, b=b, c=c, var=var, string=input_str.replace(' ',''))
        return obj

    def solve(self):
        # This is some sort of a hack, but may work out
        # We say x^2 = y and solve the quad eq
        y_eq = self.string.replace('^2', '').replace('^4', '^2')
        y1, y2 = QuadraticEquation.from_str(y_eq).solve()

        # Now solve y1 and y2
        solutions = []
        if y1 > 0:
            sol1, sol2 = sympy.sqrt(y1), -sympy.sqrt(y1)
            solutions.extend([sol1, sol2])
        elif y1 == 0:
            sol1 = sol2 = sympy.sqrt(y1)
            solutions.append(sol1)

        if y2 > 0:
            sol3, sol4 = sympy.sqrt(y2), -sympy.sqrt(y2)
            solutions.extend([sol3, sol4])
        elif y2 == 0:
            sol3 = sol4 = sympy.sqrt(y2)
            solutions.append(sol3)
        if not solutions:
            return 'No real roots'
        return solutions

