import re
import math
import sys
from collections import defaultdict
from _fractions import simplify_fraction as simplify_frac
from meta import AlgebraMeta


class Algebra(metaclass=AlgebraMeta):
    def __init__(self):
        self.SQRT_SIGN = '√'
        self.INVALID_QUADRATIC_EQUATION = 'Invalid quadratic equation!'

    def __get_primes(self, n):
        primes = []
        count = 2
        while count < n:
            isprime = True
            for x in range(2, int(math.sqrt(count) + 1)):
                if count % x == 0:
                    isprime = False
                    break
            if isprime:
                primes.append(count)
            count += 1
        return primes

    def __get_prime_delimeters(self, n):
        primes_to_n = self.__get_primes(n)
        prime_delimeters = [x for x in primes_to_n if n % x == 0]
        return prime_delimeters

    def __decompose_number(self, number):
        primes = self.__get_primes(number)
        decomposed = []
        index = 0
        while number not in primes and index < len(primes):
            while number % primes[index] == 0:
                decomposed.append(primes[index])
                number /= primes[index]
            index += 1
        decomposed.append(int(number))
        if 1 in decomposed:
            decomposed.remove(1)
        return decomposed

    def __create_histogram(self, items):
        histogram = defaultdict(int)
        for i in items:
            histogram[i] += 1
        return histogram

    def get_divisors(self, n):
        n = int(n)
        return [x for x in range(1, n + 1) if n % x == 0]

    def get_common_divisors(self, divisors_string):
        # this method is to prepare inner call so that user can call this
        # method directly

        # Numbers can be split by anything but a number e.g. : 40 $2 should
        # parse to 40, 2
        divisors = re.findall('[0-9]+', divisors_string)

        if len(divisors) != 2:
            raise ValueError('Invalid input for divisors string!')
        return self.__get_common_divisors(divisors[0], divisors[1])

    def __get_common_divisors(self, a, b):
        nominator_divisors = self.get_divisors(a)
        denominator_divisors = self.get_divisors(b)
        return sorted(list(set(nominator_divisors) & set(denominator_divisors)))

    def sqrt(self, number, calculate=False):
        if calculate:
            return math.sqrt(number)
        try:
            number = int(number)
            if number < 0:
                raise
        except:
            return 'Invalid number'
        compounds = self.__decompose_number(number)
        histogram = dict(self.__create_histogram(compounds))

        coef = 1
        under_root = 0
        for k, v in histogram.items():
            if v == 1:
                under_root *= k
            if v % 2 == 1:
                under_root += k
                v -= 1

            while v % 2 == 0 and v > 0:
                coef *= k
                v -= 2
        #print(histogram)
        #print(coef, under_root)

        # prepare answer for printing
        if coef == 1:
            return self.SQRT_SIGN + str(number)
        if under_root == 1 or under_root == 0:
            return coef
        return str(coef) + self.SQRT_SIGN + str(under_root)

    def __quadratic_equation(self, equation, var):
        split_equation = [x.replace(' ','') for x in equation.split(var)]
        try:
            a = int(split_equation[0][:-1])
            if a == 0:
                return self.INVALID_QUADRATIC_EQUATION
        except ValueError:
            a = 1
        try:
            b = int(split_equation[1].split('^2')[1][:-1])
            if b == 0:
                return self.INVALID_QUADRATIC_EQUATION
        except ValueError:
            b = 1
        try:
            c = int(split_equation[-1])
        except ValueError:
            c = 1

        d = b ** 2 - 4 * a * c

       # print(a,b,c,d)
        if d < 0:
            return 'No real roots'
        elif d == 0:
            # 1 root
            x = -b  / (2 * a)
            return 'x1 = x2 = {0}'.format(x)
        # 2 roots
        sqrt_d = self.sqrt(d)
        x1 = '({} + {}) / {}'.format(-b, sqrt_d, 2 * a)
        x2 = '({} - {}) / {}'.format(-b, sqrt_d, 2 * a)
       # Check if can be calculated if not - simplify result
        if self.SQRT_SIGN not in x1:
           x1 = eval(str(x1))
        else:
            x1 = self.__simplify_quadratic_result(sqrt_d, a, b, '+')
        if self.SQRT_SIGN not in x2:
            x2 = eval(str(x2))
        else:
            x2 = self.__simplify_quadratic_result(sqrt_d, a, b, '-')
        return 'x1 = {}\nx2 = {}'.format(x1, x2)

    # Having (4 + 4*sqrt(2)) / 2 will divide all by 2 -> 2 + 2*Sqrt(2)
    # The format sign is to format the result with the correct sign
    def __simplify_quadratic_result(self, sqrt_d, a, b, format_sign):
            split_root = sqrt_d.split(self.SQRT_SIGN)
            try:
                root_coef = int(split_root[0])
            except ValueError:
                root_coef = 1
            b_2a_divisors = self.__get_common_divisors(-b, 2 * a)
            sqrt_d_2a_divisors = self.__get_common_divisors(root_coef, 2 * a)
            common_divisors = [x for x in b_2a_divisors if x in sqrt_d_2a_divisors]
            if len(common_divisors) > 0:
                b /= max(common_divisors)
                root_coef /= max(common_divisors)
                a /= max(common_divisors)
            return ('({} {} {}{}{}) / {}'.format(int(-b), format_sign, root_coef, self.SQRT_SIGN, split_root[1], 2 * a)).replace('1.0', '')

    def quadratic_equation(self, equation):
        for letter in [chr(x) for x in range(97, 123)]:
            if letter in equation:
                return self.__quadratic_equation(equation, letter)
        return 'Invalid variable'

    def simplify_fraction(self, fraction):
        fraction = [int(x) for x in fraction.split('/')]
        if any(int(t) <= 0 for t in fraction):
            return 'Simplify fraction works with positive integers for now!'
        return simplify_frac((fraction))


def main():
    algebra = Algebra()
    # choose_math_func = input('Choose math func (sqrt/quad):')

    options = {x: algebra.methods[x] for x in range(len(algebra.methods))}

    print_str = ''
    for key in options.keys():
        print_str += '{}) {}\n'.format(key, options[key])
    method_choice = int(input(print_str + '\n' + '>>>'))
    # import ipdb; ipdb.set_trace()# BREAKPOINT)
    inp = input('Enter your problem:')
    # import ipdb; ipdb.set_trace()# BREAKPOINT)

    # print(options[method_choice](inp))

    # print(eval('algebra.{}(str({}))'.format(options[method_choice], inp)))
    # print(inp)
    # print(eval('algebra.{}('.format(options[method_choice])+ str(inp) + ')'))
    # print(inp)
    result = getattr(algebra, options[method_choice])(inp)
    print(result)
    # print(options[choose_math_func](inp))


if __name__ == '__main__':
    main()
