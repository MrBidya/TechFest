def format_inequality_result_string(and_or_expr):
    result = []
    if and_or_expr.__class__.__name__ == 'Or':
        if not and_or_expr.args:
            raise ValueError('Recieved empty Or expression. Dafk?')
        for expr in and_or_expr.args:
            # TODO: This will fail when dealing with more complex boolean
            # operations. Revise this method.
            result.append(expr.args)
    elif and_or_expr.__class__.__name__ == 'And':
        result.append(and_or_expr.args)
    return result
