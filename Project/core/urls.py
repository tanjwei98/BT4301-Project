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
    path('accuracy/', views.accuracy, name = 'accuracy'),
    path('service_health/', views.service_health, name = 'service_health'),
    path('drift/', views.datadrift, name = 'drift'),
    path('humility/', views.humility, name = 'humility'),
    path('humility/add', views.humility_add, name = 'humility_add'),
    path('challengers/', views.challengers, name = 'challengers'),
    path('challengers/modelRegistry', views.modelRegistry, name = 'modelRegistry'),
    path('codeEditor2/', views.codeEditor2, name = 'codeEditor2'),
    # path('mregistry/', views.mregistry, name = 'mregistry'),
    path('loginpage/', views.loginpage, name='loginpage'),
    path('challengers/modelRegistry/translate/', views.translate_code, name='translate_code'), # Code porting
    # path('saveas/<str:filename>',views.save_saved, name='save_saved'),
    path('challengers/saveas/',views.save_saved, name='save_saved'),
    # path('save',views.save),

    path("codeEditor2/run_code/", views.run_code, name="run_code")
    ]