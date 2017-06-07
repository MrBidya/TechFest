from django.test import TestCase, Client
from django.urls import reverse_lazy
from hypothesis.strategies import integers, floats, text, characters
from hypothesis import given
from string import ascii_letters, ascii_lowercase

# Create your tests here.
MAX_INT = 10000000
MIN_INT = -MAX_INT

class TestEquation(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse_lazy('equation_view')

    @given(text(alphabet=ascii_letters), text(alphabet=ascii_letters))
    def test_invalid_request(self, request_word, value_word):
        response = self.client.post(self.url, data={request_word: value_word})
        self.assertEqual(403, response.status_code)

    @given(integers(min_value=1))
    def test_no_real_roots_with_integers(self, number):
        response = self.client.post(self.url, data={'equation': number})
        self.assertEqual(200, response.status_code)
        self.assertEqual('No real roots', response.data['answer'])

    @given(floats(min_value=1, allow_infinity=False))
    def test_no_real_roots_with_floats(self, number):
        response = self.client.post(self.url, data={'equation': number})
        self.assertEqual(200, response.status_code)
        self.assertEqual('No real roots', response.data['answer'])

    @given(text(max_size=1, alphabet=ascii_letters), integers(min_value=1))
    def test_letter_is_in_answer(self, letter, number):
        response = self.client.post(self.url, data={'equation': '{} - {}'.format(letter, number)})
        self.assertTrue(letter.lower() in x.keys() for x in response.data['answer'])
        self.assertEqual(200, response.status_code)

class TestInequality(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse_lazy('inequality_view')

    @given(text(alphabet=ascii_lowercase, max_size=1), integers(max_value=MAX_INT))
    def test_linear_inequality_with_random_letter(self, letter, number):
        if letter == '':
            return
        response = self.client.post(self.url, data={"inequality" : '{}>{}'.format(letter, number)})
        self.assertEqual(200, response.status_code)
        self.assertEqual([{'{}1'.format(letter):'({} < {}, {} < oo)'.format(number, letter, letter)}], response.data['answer'])

    @given(integers(min_value=MIN_INT, max_value=MAX_INT))
    def test_quadratic_inequality(self, num):
        # Fix the case where D<0
        num2 = 4 * num
        response = self.client.post(self.url, data={"inequality" : 'x^2 - {}*x - {}>0'.format(num2, num)})
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data['answer']))

    @given(integers(min_value=0, max_value=MAX_INT), integers(min_value=0, max_value=MAX_INT))
    def test_any_value_is_a_solution(self,num, num2):
        response = self.client.post(self.url, data={"inequality" : '{}*x^2+ {} + 1>0'.format(num, num2)})
        self.assertEqual(200, response.status_code)
        self.assertEqual('Any value is a solution', response.data['answer'])
