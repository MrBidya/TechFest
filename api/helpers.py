from core.algebra.exceptions import NoRealRootsException
from core.algebra.parser import validate_equation
from core.algebra.algebra import Equation, Inequality

def solve_eq(equation):
    if not equation:
        # throw exception or return '' ?
        return ''
    eq = Equation(equation)
    result = eq.solve()
    return result, eq.get_eq_vars()


def solve_ie(inequality):
    if not inequality:
        return ''
    ie = Inequality(inequality)
    result = ie.solve()
    if not result:
        result = 'No real roots'
    return result, ie.get_ie_var()


