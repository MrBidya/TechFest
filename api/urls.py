from django.conf.urls import include, url
from .views import IndexView, EquationView, InequalityView


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index_view'),
    url(r'solve/equation/$', EquationView.as_view(), name='equation_view'),
    url(r'solve/inequality/$', InequalityView.as_view(), name='inequality_view')
]
