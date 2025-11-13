from django.urls import path
from . import views

app_name = 'leituras'

urlpatterns = [
    path('', views.index, name='index'),
    path('agregar-leituras/', views.agregar, name='agregar'),
    path('exportar-leituras/', views.exportar, name='exportar'),
]
