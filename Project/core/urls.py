from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, re_path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('main/', views.index, name='main'),
    path('form/', views.form, name='form'),
    path('card/', views.card, name='card'),
    path('chart/', views.chart, name='chart'),
    path('button/', views.button, name='button'),
    path('modal/', views.modal, name='modal'),
    path('table/', views.table, name='table'),
    path('deployment/', views.deployment, name = 'deployment'),
    path('overview/', views.overview, name = 'overview'),
    path('overview/accuracy', views.accuracy, name = 'accuracy'),
    path('overview/service_health', views.service_health, name = 'service_health')
    
]