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
def drift_importance(ProjectName, start_date = datetime(2023,4,5), end_date = datetime(2023,4,7)):
    model_id = Model_List.objects.filter(Project_Name = ProjectName, Challenger_Status = 'Champion').first().Model_ID
    drift_data = pd.DataFrame(list(Model_drift.objects.filter(Model_ID_id = model_id).values()))
    drift_data["Date"] = pd.to_datetime(drift_data['Date']).dt.date
    drift_data["Date"] = pd.to_datetime(drift_data['Date'])
    # start_date = datetime(2023,4,5)
    # end_date = datetime(2023,4,7)

    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    if start_date < datetime(2023,4,5):
        start_date = datetime(2023,4,5)
    
    if end_date > datetime(2023,4,7):
        end_date = datetime(2023,4,7)

    after_start_date = drift_data["Date"] >= (start_date - dt.timedelta(days=1))
    before_end_date = drift_data["Date"] <= end_date
    filtered_dataset = drift_data[after_start_date & before_end_date]
    grouped = filtered_dataset.groupby("Feature").mean().reset_index()
    all_features = list(grouped["Feature"])

    at_risk = grouped[grouped["Drift"] > 0.5]
    passing = grouped[grouped["Drift"] <= 0.5]
    
    passing_drift = list(passing["Drift"])
    passing_importance = list(passing["Importance"])
    passing_features = list(passing["Feature"])

    at_risk_drift = list(at_risk["Drift"])
    at_risk_importance = list(at_risk["Importance"])
    at_risk_features = list(at_risk["Feature"])

    return {"passing_drift": passing_drift, "passing_importance": passing_importance, "passing_feature": passing_features,
            'at_risk_drift': at_risk_drift, 'at_risk_importance': at_risk_importance, 'at_risk_feature': at_risk_features,
            'all_feature': all_features}

def feature_distribution(ProjectName, start_date = datetime(2023,4,5), end_date = datetime(2023,4,7)):
    model_id = Model_List.objects.filter(Project_Name = ProjectName, Challenger_Status = 'Champion').first().Model_ID
    feature_dist_data = pd.DataFrame(list(Feature_Distribution.objects.filter(Model_ID_id = model_id).values()))
    feature_dist_data["Date"] = pd.to_datetime(feature_dist_data['Date']).dt.date
    feature_dist_data["Date"] = pd.to_datetime(feature_dist_data['Date'])
    # start_date = datetime(2023,4,5)
    # end_date = datetime(2023,4,7)
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    if start_date < datetime(2023,4,5):
        start_date = datetime(2023,4,5)
    if start_date >= datetime(2023,4,7):
        start_date = datetime(2023,4,6)
    
    if end_date > datetime(2023,4,7):
        end_date = datetime(2023,4,7)
    if end_date <= datetime(2023,4,5):
        end_date = datetime(2023,4,6)

    after_start_date = feature_dist_data["Date"] >= (start_date - dt.timedelta(days=1))
    before_end_date = feature_dist_data["Date"] <= end_date
    filtered_dataset = feature_dist_data[after_start_date & before_end_date]
    #print(filtered_dataset.columns)
    grouped = filtered_dataset.groupby("Feature_values").mean().reset_index()

    feature_values = list(grouped["Feature_values"])
    training_distribution = list(grouped["train_distribution"])
    scoring_distribution = list(grouped["actual_distribution"])
    feature = feature_dist_data["Feature"].iloc[0]

    return {"train_dist": training_distribution, "scoring_dist": scoring_distribution, "feature_values": feature_values, 'feature': feature}