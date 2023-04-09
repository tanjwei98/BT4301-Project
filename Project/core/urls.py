from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, re_path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('login/', views.userlogin, name='login'),
    path('logout/', views.userlogout, name = 'logout'),
    path('deployment/', views.deployment, name = 'deployment'),
    path('overview/<Project_Name>/', views.overview, name = 'overview'),
    path('overview/<model_name>/approve-model/', views.approveModel, name = 'approveModel'),
    path('accuracy/<Project_Name>/', views.accuracy, name = 'accuracy'),
    path('accuracy/<Project_Name>/accuracy_chart/', views.accuracy_chart, name='accuracy_chart'),
    path('service_health/<Project_Name>/', views.service_health, name = 'service_health'),
    path('service_health/<Project_Name>/service_chart', views.service_chart, name = 'service_chart'),
    path('drift/<Project_Name>/', views.datadrift, name = 'drift'),
    path('humility/<Project_Name>/', views.humility, name = 'humility'),
    path('humility/<Project_Name>/add', views.humility_add, name = 'humility_add'),
    path('challengers/<Project_Name>/', views.challengers, name = 'challengers'),
    path('challengers/<Project_Name>/modelRegistry', views.modelRegistry, name = 'modelRegistry'),
    path('challengers/<Project_Name>/modelRegistry/get_dataset_info/', views.get_dataset_info, name = 'get_dataset_info'),
    path('challengers/<Project_Name>/challenger_chart', views.challenger_chart, name = 'challenger_charts'),
    path('codeEditor2/', views.codeEditor2, name = 'codeEditor2'),
    path('challengers/<Project_Name>/modelRegistry/translate/', views.translate_code, name='translate_code'), # Code porting
    path('challengers/<Project_Name>/modelRegistry/add-model/', views.addModel, name='addModel'), # Add model into database
    path('challengers/<Project_Name>/saveas/',views.save_saved, name='save_saved'),
    path('challengers/<Project_Name>/make_champion_model/',views.make_champion_model, name='make_champion'),
    path("codeEditor2/run_code/", views.run_code, name="run_code")
    ]