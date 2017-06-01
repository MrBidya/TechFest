from sympy import simplify, Eq


class Parser(object):
    @staticmethod
    def solve(validated_input_str):
        # Escape input_str
        # Start doing real shit

        # Check if equation is passed with right and left side
        split_equation = validated_input_str.split('=')
        if len(split_equation) == 2:
            # Has right side
            equation = Eq(simplify(split_equation[0], simplify(split_equation[1])))
        else:
            equation = simplify(validated_input_str)


def validate_equation(input_str):
    # Do some stuff to avoid trouble
    return input_str


def validate_inequality(input_str):
    # Do some stuff to avoid trouble
    return input_str


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
