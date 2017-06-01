import importlib
from sympy.core.numbers import Integer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

# Create your views here.
from .helpers import solve_eq, solve_ie
from core.algebra.exceptions import ProblemMessageException
from api.mixins import UsageMixin
from collections import OrderedDict



class IndexView(UsageMixin, APIView):
    def get(self, request):
        from .urls import urlpatterns
        data = {"available endpoints": []}

        for endpoint in urlpatterns:
            # Extract class -> 'api.views.IndexView' -> IndexView
            split_lookup_str = endpoint.lookup_str.split('.')
            klass = getattr(importlib.import_module('.'.join(split_lookup_str[:-1])), split_lookup_str[-1])

            endpoint_dict = OrderedDict()
            endpoint_dict['name'] = klass.__name__
            endpoint_dict['allowed methods'] = klass._allowed_methods(klass)
            # Hard coding the /api/ part because how do you get the full regex
            # when you are including the urls?
            endpoint_dict['regex'] = '/api/' + endpoint.regex.pattern

            endpoint_dict['usage'] = klass.get_usage()
            endpoint_dict['example'] = klass.get_example()
            data["available endpoints"].append(endpoint_dict)
        return Response(data=data)

    @classmethod
    def get_usage(cls):
        return 'GET me to view this information'


class EquationView(UsageMixin, APIView):
    usage_type = 'a*x - b'
    usage_example = '10*x-2'

    def post(self, request):
        request_eq = request.data.get('equation')
        if not request_eq:
            return Response(data={'You must pass a keyvalue pair with key "equation" and the actual equation as value string' }, status=403)
        # Return format:

        #{
        #    "answer":[
        #        {"x1" : 2},
        #        {"x2" : 3}
        #    ]
        #}

        # solve_eq returns ([answer1, answer2...], eq_vars)
        try:
            solved_eq = solve_eq(request_eq.lower())
        except ProblemMessageException as e:
            data = {"answer" : str(e), 'status': 200}
        except Exception as e:
            data = {"errors": str(e), 'status': 400}
        else:
            result, eq_vars = solved_eq
            data = {"answer": [{"{}{}".format(eq_vars[0], index + 1):int(value) if type(value) == Integer else str(value)} for index, value in enumerate(result)], 'status': 200}
        return Response(data=data, status=data['status'])


class InequalityView(UsageMixin, APIView):
    usage_type = 'a*x - b < c'
    usage_example = '10*x - 2 < 3'

    def post(self, request):
        request_ie = request.data.get('inequality')
        if not request_ie:
            return Response(data={'You must pass a keyvalue pair with key "inequality" and the actual equation as value string' }, status=403)

        # solve_eq returns ([answer1, answer2...], eq_vars)
        try:
            solved_ie = solve_ie(request_ie)
        except ProblemMessageException as e:
            data = {"answer" : str(e), 'status': 200}
        except Exception as e:
            data = {"errors": str(e), 'status': 400}
        else:
            result, ie_var = solved_ie
            if result == 'No real roots':
                data = {"answer": result, 'status': 200}
            else:
                data = {"answer": [{"{}{}".format(ie_var, index + 1):int(value) if type(value) == Integer else str(value)} for index, value in enumerate(result)], 'status': 200}
        return Response(data=data, status=data['status'])
