from django.contrib import admin

# Register your models here.
from .models import Dataset_List, Users, Model_List, Service_Health, Model_Accuracy, Feature_Distribution, Model_drift

admin.site.register(Dataset_List)
admin.site.register(Users)
admin.site.register(Model_List)
admin.site.register(Service_Health)
admin.site.register(Model_Accuracy)
admin.site.register(Feature_Distribution)
admin.site.register(Model_drift)
