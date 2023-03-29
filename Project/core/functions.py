from .models import *

# Deployment page
def get_deployments(userID):
    no_of_deployments = Model_List.objects.filter(User_ID = userID).count()
    
    return {"no_of_deployments": no_of_deployments}

def get_service_health(userID):
    SH_pass = Model_List.objects.filter(User_ID = userID, Service_Health_Status = "Passing").count()
    SH_at_risk = Model_List.objects.filter(User_ID = userID, Service_Health_Status = "At Risk").count()
    SH_fail = Model_List.objects.filter(User_ID = userID, Service_Health_Status = "Failing").count()
    
    return {"SH_Pass": SH_pass, "SH_At_Risk": SH_at_risk, "SH_Fail": SH_fail}

def get_data_drift(userID):
    DD_pass = Model_List.objects.filter(User_ID = userID, Data_Drift_Status = "Passing").count()
    DD_at_risk = Model_List.objects.filter(User_ID = userID, Data_Drift_Status = "At Risk").count()
    DD_fail = Model_List.objects.filter(User_ID = userID, Data_Drift_Status = "Failing").count()
    
    return {"DD_Pass": DD_pass, "DD_At_Risk": DD_at_risk, "DD_Fail": DD_fail}

def get_accuracy(userID):
    A_pass = Model_List.objects.filter(User_ID = userID, Accuracy_Status = "Passing").count()
    A_at_risk = Model_List.objects.filter(User_ID = userID, Accuracy_Status = "At Risk").count()
    A_fail = Model_List.objects.filter(User_ID = userID, Accuracy_Status = "Failing").count()
    
    return {"A_Pass": A_pass, "A_At_Risk": A_at_risk, "A_Fail": A_fail}

def deployed_models(userID):
    models = Model_List.objects.filter(User_ID = userID)
    return {"Deployed_Models": models}

