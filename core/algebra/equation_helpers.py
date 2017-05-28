import re


def prepare_input(input_str):
    # This method has to do any preparation to input_str so that is makes no
    # trouble while it is being parsed
    input_str = input_str.replace(' ', '')
    return input_str



def extract_var(input_str):
    for letter in [chr(x) for x in range(97, 123)]:
        # lower lowers all letters
        if letter in input_str.lower():
            return letter
    raise ValueError('Cannot parse equation variable')


def get_quad_coeffs(input_str, eq_var):
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
        elif b == '+':
            b = 1
    # This takes the last number.
    # IMPORTANT:
    # The input string MUST be in valid format or else it will break
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


