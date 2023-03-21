from django.db import models
import pytz

utc=pytz.UTC

# Create your models here.

class Dataset_List(models.Model):
    Dataset_name = models.CharField(max_length=255)
    Dataset_id = models.CharField(max_length=255,primary_key=True)
    num_of_rows = models.IntegerField()
    num_of_features = models.IntegerField()
 
class Users(models.Model):
    User_ID = models.CharField(max_length=255,primary_key=True)
    Name = models.CharField(max_length=255,null=False)
    Password = models.CharField(max_length=255,null=False)
    Role = models.CharField(max_length=255,null=False)
 
class Model_List(models.Model):
    Model_ID = models.CharField(max_length=255,primary_key=True)
    Model_name = models.CharField(max_length=255,null=False)
    Model_version = models.CharField(max_length=255,null=False)
    Language = models.CharField(max_length=255,null=False)
    User_ID = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    Dataset_id=models.ForeignKey(Dataset_List, on_delete=models.DO_NOTHING)

class Service_Health(models.Model):
    Response_time = models.CharField(max_length=255,null=False)
    Execution_time = models.CharField(max_length=255,null=False)
    Data_error_rate = models.FloatField(max_length=255,null=False)
    System_error_rate = models.FloatField(max_length=255,null=False)
    Total_predictions = models.CharField(max_length=255,null=False)
    Date = models.DateTimeField(null=False) 
    Location = models.CharField(max_length=255,null=False)
    Model_ID = models.ForeignKey(Model_List, on_delete=models.DO_NOTHING)
    Dataset_id=models.ForeignKey(Dataset_List, on_delete=models.DO_NOTHING)

class Model_Accuracy(models.Model):
    LogLoss = models.FloatField(max_length=255,null=False)
    AUC = models.FloatField(max_length=255,null=False)
    KS = models.FloatField(max_length=255,null=False)
    Gini_Norm = models.FloatField(max_length=255,null=False)
    Rate_Top10 = models.FloatField(max_length=255,null=False)
    Date = models.DateTimeField(null=False) 
    Location = models.CharField(max_length=255,null=False)
    Target = models.CharField(max_length=255,null=False)
    Predicted = models.CharField(max_length=255,null=False)
    Model_ID = models.ForeignKey(Model_List, on_delete=models.DO_NOTHING)
    Dataset_id=models.ForeignKey(Dataset_List, on_delete=models.DO_NOTHING)

class Feature_Distribution(models.Model):
    train_distribution= models.FloatField(max_length=255,null=False)
    actual_distribution= models.CharField(max_length=255,null=False)
    Date= models.DateTimeField(max_length=255,null=False)
    Feature= models.CharField(max_length=255,null=False)
    Model_ID = models.ForeignKey(Model_List, on_delete=models.DO_NOTHING)
    Dataset_id=models.ForeignKey(Dataset_List, on_delete=models.DO_NOTHING)

class Model_drift(models.Model):
    Feature= models.CharField(max_length=255,null=False)
    Drift= models.FloatField(max_length=255,null=False)
    Importance= models.FloatField(max_length=255,null=False)
    Date= models.DateTimeField(max_length=255,null=False)
    Model_ID = models.ForeignKey(Model_List, on_delete=models.DO_NOTHING)
    Dataset_id=models.ForeignKey(Dataset_List, on_delete=models.DO_NOTHING)