from core.algebra.equation import Equation
from core.algebra.exceptions import EquationNotSupportedException, NoRealRootsException

def solve_eq(equation):
    if not equation:
        # throw exception or return '' ?
        return ''
    try:
        eq = Equation.from_str(equation)
        # Equation type is determined by the highest power(eq must be
        # normalized so the highest power is first, or problems may occur)
        result = eq.solve()
        # Return eq.var so the view can print the corrent letter
        return result, eq.var
    except EquationNotSupportedException as e:
        result = e
    except NoRealRootsException as e:
        result = e
    except ValueError as e:
        result = str(e)
    return result,

