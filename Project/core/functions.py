from .models import *
import datetime as dt
from datetime import date, datetime
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


# Deployment page
def get_deployments(userID, userRole):
    if userRole == "MLOps Engineer":
        no_of_deployments = Model_List.objects.filter(Approve_User_ID_id = userID).count()
    else:
        no_of_deployments = Model_List.objects.filter(User_ID = userID).count()
    
    return {"no_of_deployments": no_of_deployments}

def get_service_health(userID, userRole):
    if userRole == "MLOps Engineer":
        SH_pass = Model_List.objects.filter(Approve_User_ID_id = userID, Service_Health_Status = "Passing").count()
        SH_at_risk = Model_List.objects.filter(Approve_User_ID_id = userID, Service_Health_Status = "At Risk").count()
        SH_fail = Model_List.objects.filter(Approve_User_ID_id = userID, Service_Health_Status = "Failing").count()
    else:
        SH_pass = Model_List.objects.filter(User_ID = userID, Service_Health_Status = "Passing").count()
        SH_at_risk = Model_List.objects.filter(User_ID = userID, Service_Health_Status = "At Risk").count()
        SH_fail = Model_List.objects.filter(User_ID = userID, Service_Health_Status = "Failing").count()
    
    return {"SH_Pass": SH_pass, "SH_At_Risk": SH_at_risk, "SH_Fail": SH_fail}

def get_data_drift(userID, userRole):
    if userRole == "MLOps Engineer":
        DD_pass = Model_List.objects.filter(Approve_User_ID_id = userID, Data_Drift_Status = "Passing").count()
        DD_at_risk = Model_List.objects.filter(Approve_User_ID_id = userID, Data_Drift_Status = "At Risk").count()
        DD_fail = Model_List.objects.filter(Approve_User_ID_id = userID, Data_Drift_Status = "Failing").count()
    else:
        DD_pass = Model_List.objects.filter(User_ID = userID, Data_Drift_Status = "Passing").count()
        DD_at_risk = Model_List.objects.filter(User_ID = userID, Data_Drift_Status = "At Risk").count()
        DD_fail = Model_List.objects.filter(User_ID = userID, Data_Drift_Status = "Failing").count()
    
    return {"DD_Pass": DD_pass, "DD_At_Risk": DD_at_risk, "DD_Fail": DD_fail}

def get_accuracy(userID, userRole):
    if userRole == "MLOps Engineer":
        A_pass = Model_List.objects.filter(Approve_User_ID_id = userID, Accuracy_Status = "Passing").count()
        A_at_risk = Model_List.objects.filter(Approve_User_ID_id = userID, Accuracy_Status = "At Risk").count()
        A_fail = Model_List.objects.filter(Approve_User_ID_id = userID, Accuracy_Status = "Failing").count()
    else:
        A_pass = Model_List.objects.filter(User_ID = userID, Accuracy_Status = "Passing").count()
        A_at_risk = Model_List.objects.filter(User_ID = userID, Accuracy_Status = "At Risk").count()
        A_fail = Model_List.objects.filter(User_ID = userID, Accuracy_Status = "Failing").count()
    
    return {"A_Pass": A_pass, "A_At_Risk": A_at_risk, "A_Fail": A_fail}

def deployed_models(userID, userRole):
    if userRole == "MLOps Engineer":
        models = Model_List.objects.filter(Approve_User_ID_id = userID)
    else:
        models = Model_List.objects.filter(User_ID = userID)
    return {"Deployed_Models": models}

# Overview page
def get_model(ProjectName):
    model = Model_List.objects.filter(Project_Name = ProjectName, Challenger_Status = 'Champion').first()
    return {"Model": model}

def get_dataset(ProjectName):
    dataset_id = Model_List.objects.filter(Project_Name = ProjectName, Challenger_Status = 'Champion').first().Dataset_ID_id
    dataset = Dataset_List.objects.filter(Dataset_ID = dataset_id).first()
    return {"Dataset": dataset}

# Data Drift page
def drift_importance(ProjectName, start_date = date(2023,4,5), end_date = date(2023,4,7)):
    model_id = Model_List.objects.filter(Project_Name = ProjectName, Challenger_Status = 'Champion').first().Model_ID
    drift_data = pd.DataFrame(list(Model_drift.objects.filter(Model_ID_id = model_id).values()))
    drift_data["Date"] = pd.to_datetime(drift_data['Date']).dt.date
    drift_data["Date"] = pd.to_datetime(drift_data['Date'])
    start_date = datetime(2023,4,5)
    end_date = datetime(2023,4,7)
    after_start_date = drift_data["Date"] >= (start_date - dt.timedelta(days=1))
    before_end_date = drift_data["Date"] <= end_date
    filtered_dataset = drift_data[after_start_date & before_end_date]
    grouped = filtered_dataset.groupby("Feature").mean().reset_index()
    drift = list(grouped["Drift"])
    importance = list(grouped["Importance"])
    features = list(grouped["Feature"])

    return {"Drift": drift, "Importance": importance, "Feature": features}