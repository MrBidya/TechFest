from django.conf.urls import include, url
from .views import IndexView, EquationView


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index_view'),
    url(r'solve/equation', EquationView.as_view(), name='quad_eq_view'),
]
