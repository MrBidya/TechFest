from django.test import TestCase, Client
from django.urls import reverse_lazy
from hypothesis.strategies import integers, floats, text, characters
from hypothesis import given
from string import ascii_letters

# Create your tests here.

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
