from django.conf.urls import include, url
from .views import IndexView, QuadradricEquationView


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index_view'),
    url(r'solve/quad-equation', QuadradricEquationView.as_view(), name='quad_eq_view'),
]
