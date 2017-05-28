import re
#from core.algebra.equation import LinearEquation, QuadraticEquation, BiquadraticEquation


def prepare_input(input_str, eq_type):
    # This method has to do any preparation to input_str so that is makes no
    # trouble while it is being parsed

    # Some trouble importing stuff so doing some hackery stuff with python
    eq_type_to_prepare_func = {
                                'LinearEquation' : prepare_linear_eq,
                                'QuadraticEquation' : prepare_quad_eq,
                                'BiquadraticEquation' : prepare_bidquad_eq
                                }
    prepared_input = eq_type_to_prepare_func[eq_type.__name__](input_str)
    return prepared_input


def prepare_quad_eq(input_str):
    '''
    x^2-x-1 => 1*x^2-1*x-1
    '''
    eq_var = extract_var(input_str)
    split_by_var = input_str.split(eq_var)

    # Check if coeff A is passed
    if split_by_var[0] == '':
        input_str = '1*' + input_str
        split_by_var = input_str.split(eq_var)
    # Check if coeff A is passed with * sign
    if '*' not in split_by_var[0]:
        split_by_var[0] = split_by_var[0] + '*'
        input_str = eq_var.join(split_by_var)

    # Check if coeff B is passed
    second_part = len(re.findall(r'\d+', split_by_var[1]))
    if second_part < 2:
        split_by_var[1] = split_by_var[1] + '1*'
        input_str = eq_var.join(split_by_var)
    elif second_part == 2 and split_by_var[1][-1] != '*':
        split_by_var[1] = split_by_var[1] + '*'
        input_str = eq_var.join(split_by_var)

    return input_str


def prepare_bidquad_eq(input_str):
    pass


def prepare_linear_eq(input_str):
    pass



def extract_var(input_str):
    for letter in [chr(x) for x in range(97, 123)]:
        # lower lowers all letters
        if letter in input_str.lower():
            return letter
    raise ValueError('Cannot parse equation variable')


def get_quad_coeffs(input_str, eq_var):
    # Make sure input is validated before calling this function
    # Valid quad equation looks like this "ax^n + bx + c" where n = 2,4;
    eq_power = get_eq_power(input_str)
    try:
        a = int(input_str[:input_str.index(eq_var)].replace('*', ''))
    except ValueError:
        if input_str[0] == '-':
            a = -1
        else:
            a = 1

    try:
        b = input_str.split(eq_var)[1].split(str(eq_power))[1].replace('*', '')
        b = int(b)
    except ValueError:
        if b == '-':
            b = -1
        else:
            b = 1
    # This takes the last number.
    # IMPORTANT:
    # The input string MUST be in valid format or else it may break
    match = re.search(r'\d+$', input_str)
    if match is not None:
        c = int(match.group())
    else:
        c = 0
    return a, b, c


def get_eq_power(input_str):
    # 'x^4 - x^2 - 10' will return 4
    power = int(re.match('\d+', input_str.split('^')[1]).group())
    return power


