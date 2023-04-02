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
    #path(r'overview/?P<model_id>[a-z0-9]*/>', views.overview, name = 'overview'),
    path('overview/<model_Name>/', views.overview, name = 'overview'),
    path('overview/approve-model/', views.approveModel, name = 'approveModel'),
    path('accuracy/', views.accuracy, name = 'accuracy'),
    path('accuracy/accuracy_chart/', views.accuracy_chart, name='accuracy_chart'),
    path('accuracy/predicted_actual_chart/', views.predicted_actual_chart, name='predicted_actual_chart'),
    path('service_health/', views.service_health, name = 'service_health'),
    path('service_health/service_chart', views.service_chart, name = 'service_chart'),
    path('drift/<model_Name>/', views.datadrift, name = 'drift'),
    path('humility/', views.humility, name = 'humility'),
    path('humility/add', views.humility_add, name = 'humility_add'),
    path('challengers/', views.challengers, name = 'challengers'),
    path('challengers/modelRegistry', views.modelRegistry, name = 'modelRegistry'),
    path('codeEditor2/', views.codeEditor2, name = 'codeEditor2'),
    # path('mregistry/', views.mregistry, name = 'mregistry'),
    #path('login/', views.loginpage, name='loginpage'),
    path('login/', views.userlogin, name='login'),
    path('logout/', views.userlogout, name = 'logout'),
    path('challengers/modelRegistry/translate/', views.translate_code, name='translate_code'), # Code porting
    path('challengers/modelRegistry/add-model/', views.addModel, name='addModel'), # Add model into database
    # path('saveas/<str:filename>',views.save_saved, name='save_saved'),
    path('challengers/saveas/',views.save_saved, name='save_saved'),
    # path('save',views.save),

    path("codeEditor2/run_code/", views.run_code, name="run_code")
    ]