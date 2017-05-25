import algebra as a
import unittest
from string import ascii_letters
from hypothesis import given
from hypothesis.strategies import text, integers, just, sampled_from


class AlgebraTests(unittest.TestCase):
    def setUp(self):
       self.algebra = a.Algebra()

    @given(integers(min_value=2, max_value=30))
    def test_sqrt_exact_number(self, inp):
        self.assertEqual(inp, self.algebra.sqrt(inp * inp))

    @given(integers(max_value=-1))
    def test_sqrt_invalid_number(self, inp):
        self.assertEqual('Invalid number', self.algebra.sqrt(inp))

    @given(text(alphabet=ascii_letters))
    def test_sqrt_not_a_number(self, text):
        self.assertEqual('Invalid number', self.algebra.sqrt(text))

    @given(integers(min_value=2, max_value=60))
    def test_sqrt_root_of_non_squarable(self, inp):
        res = self.algebra.sqrt(inp * inp + 1)
        assert self.algebra.SQRT_SIGN in res

    def test_quadratic_equation_2_real_roots(self):
        self.assertEqual('x1 = (6 + 2.0√2) / 5.0\nx2 = (6 - 2.0√2) / 5.0', self.algebra.quadratic_equation('25 * x ^ 2 - 60 * x + 28'))

    def test_quadratic_equation_2_natural_roots(self):
        self.assertEqual('x1 = 13.0\nx2 = 2.0', self.algebra.quadratic_equation('x^2 - 15 * x + 26'))

    @given(integers(min_value=1), integers(min_value=3, max_value=4), integers(min_value=17))
    def test_quadratic_equation_no_roots(self, a, b, c):
        assert self.algebra.quadratic_equation('{}*x^2 + {}*x + {}'.format(a, b ,c)) == 'No real roots'

if __name__ == '__main__':
    unittest.main()
    pass



# test_add_one()

