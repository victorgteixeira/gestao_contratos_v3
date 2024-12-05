from django.urls import path
from . import views

urlpatterns = [
    path('top-gastos/', views.top_contratos_view, name='top_contratos_view'),
]
