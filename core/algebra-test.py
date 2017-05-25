import algebra as a
import unittest
from string import ascii_letters
from hypothesis import given
from hypothesis.strategies import text, integers, just, sampled_from
from algebra import QuadraticEquation


# Todo: write algebra tests
class QuadraticEquationTests(unittest.TestCase):
    def setUp(self):
       self.algebra = a.Algebra()

    def test_quadratic_equation_2_real_roots(self):
        self.assertEqual('(2*sqrt(2)/5 + 6/5, -2*sqrt(2)/5 + 6/5)', str(QuadraticEquation.from_str('25 * x ^ 2 - 60 * x + 28').solve()))

    def test_quadratic_equation_2_natural_roots(self):
        self.assertEqual((13, 2), QuadraticEquation.from_str('x^2 - 15 * x + 26').solve())

    @given(integers(min_value=1), integers(min_value=3, max_value=4), integers(min_value=17))
    def test_quadratic_equation_no_roots(self, a, b, c):
        eq = QuadraticEquation.from_str('{}*x^2 + {}*x + {}'.format(a, b ,c))
        self.assertRaises(ValueError,eq.solve)

if __name__ == '__main__':
    unittest.main()

