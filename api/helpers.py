from core.algebra import QuadraticEquation

def solve_quad_eq(equation):
    if not equation:
        # throw exception or return '' ?
        return ''
    try:
        result = QuadraticEquation.from_str(equation).solve()
    except ValueError:
        result = 'No real roots'
    return result
