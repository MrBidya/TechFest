from sympy.core.numbers import Integer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

# Create your views here.
from .helpers import solve_eq


class IndexView(APIView):
    def get(self, request):
        from .urls import urlpatterns
        data = {"available endpoints": [x.regex.pattern for x in urlpatterns]}
        # TODO: can add description to each endpoint and how it should be used
        return Response(data=data)


class EquationView(APIView):
    def post(self, request):
        eq = request.data.get('equation')
        if not eq:
            return Response(data={'You must pass a keyvalue pair with key "equation" and the actual equation as value string' })
        # Return format:

        #{
        #    "answer":[
        #        {"x1" : 2},
        #        {"x2" : 3}
        #    ]
        #}
        result, eq_var = solve_eq(request.data.get('equation'))
        if result == 'No real roots':
            data = {"answer": result}
        else:
            data = {"answer": [{"{}{}".format(eq_var, index + 1):int(value) if type(value) == Integer else str(value)} for index, value in enumerate(result)]}
        return Response(data=data)


