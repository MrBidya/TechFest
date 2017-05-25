import re
import math
import sys
import sympy
from collections import defaultdict
from _fractions import simplify_fraction as simplify_frac
from meta import AlgebraMeta


class Algebra(metaclass=AlgebraMeta):
    def __init__(self):
        self.SQRT_SIGN = '√'

    def get_primes(self, n):
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

    def get_prime_delimeters(self, n):
        primes_to_n = self.get_primes(n)
        prime_delimeters = [x for x in primes_to_n if n % x == 0]
        return prime_delimeters

    def decompose_number(self, number):
        primes = self.get_primes(number)
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

    def create_histogram(self, items):
        histogram = defaultdict(int)
        for i in items:
            histogram[i] += 1
        return histogram

    def get_divisors(self, n):
        n = int(n)
        return [x for x in range(1, n + 1) if n % x == 0]

    def get_common_divisors(self, divisors_string):
        # This method prepares inner call so that user can call this
        # method directly

        # Numbers can be split by anything but a number e.g. : 40 $2 should
        # parse to (40, 2)
        divisors = re.findall('[0-9]+', divisors_string)

        if len(divisors) != 2:
            raise ValueError('Invalid input for divisors string!')
        return self.__get_common_divisors(divisors[0], divisors[1])

    def __get_common_divisors(self, a, b):
        nominator_divisors = self.get_divisors(a)
        denominator_divisors = self.get_divisors(b)
        return sorted(list(set(nominator_divisors) & set(denominator_divisors)))


    def simplify_fraction(self, fraction):
        fraction = [int(x) for x in fraction.split('/')]
        if any(int(t) <= 0 for t in fraction):
            return 'Simplify fraction works with positive integers for now!'
        return simplify_frac((fraction))


class QuadraticEquation:
    def __init__(self, a=1, b=1, c=1, var='x', res1=None, res2=None, string=None):
        self.SQRT_SIGN = '√'
        self.INVALID_QUADRATIC_EQUATION = 'Invalid quadratic equation!'

        self.a = a
        self.b = b
        self.c = c
        self.var = var
        self.res1 = res1
        self.res2 = res2
        if string is not None:
            self.string = string
        else:
            self.string = '{}*{}^2 {}*{} {}'.format(self.a, self.var, self.b, self.var, self.c)

    def __repr__(self):
        return self.string

    def __str__(self):
        return self.__repr__()

    def solve(self):
        d = self.b ** 2 - 4 * self.a * self.c
        if d < 0:
            raise ValueError('No real roots')
        self.res1 = (-self.b + sympy.sqrt(d)) / (2 * self.a)
        self.res2 = (-self.b - sympy.sqrt(d)) / (2 * self.a)

        return self.res1, self.res2


    @staticmethod
    def __extract_var(input_str):
        for letter in [chr(x) for x in range(97, 123)]:
            # lower lowers all letters
            if letter in input_str.lower():
                return letter
        raise ValueError('Cannot parse equation variable')

    @staticmethod
    def __get_quad_coeffs(input_str):
        var = QuadraticEquation.__extract_var(input_str)
        try:
            a = int(input_str[:input_str.index(var)].replace('*', ''))
        except ValueError:
            if input_str[0] == '-':
                a = -1
            else:
                a = 1

        try:
            b = input_str.split(var)[1].split('^2')[1].replace('*', '')
            b = int(b)
        except ValueError:
            if b == '-':
                b = -1
            elif b == '+':
                b = 1
        # This takes the last number.
        # IMPORTANT:
        # The input string MUST be in valid format or else it will break
        c = int(re.findall(r'[-+]*\d+', input_str)[-1])
        return a, b, c


    @staticmethod
    def from_str(input_str, var=None):
        # Extract var if not passed
        input_str = input_str.replace(' ','')
        if var is None:
            var = QuadraticEquation.__extract_var(input_str)
        coefs = re.findall(r'-?[0-9]+', input_str)
        if len(coefs) != 4:
            a, b, c = QuadraticEquation.__get_quad_coeffs(input_str)
#            raise ValueError('Not enough coefficients passed. Must be 4, instead got {}'.format(len(coefs)))
        else:
        # Coefs contains the following:
            # index 0 is a
            a = int(coefs[0])
            # index 1 is the power of x which must be always 2
            # index 2 is b
            b = int(coefs[2])
            # index 3 is c
            c = int(coefs[3])

        return QuadraticEquation(a=a, b=b, c=c, var=var, string=input_str.replace(' ',''))
