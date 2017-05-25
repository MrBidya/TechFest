from core.algebra import QuadraticEquation

def solve_quad_eq(equation):
    if not equation:
        # throw exception or return '' ?
        return ''
    result = QuadraticEquation.from_str(equation).solve()
    return result
