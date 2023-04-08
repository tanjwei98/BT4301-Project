import json
import re
import subprocess
from pathlib import Path
import pandas as pd
import os
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from os import path
import pscript
import sys
from io import StringIO
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.db import connection
from .functions import *
from django.utils import timezone
from datetime import datetime
# from models import Model_Accuracy
from django.http import HttpResponseRedirect
from django.urls import reverse
import numpy as np

# Create your views here.


def index(request):
    return render(request, "index.html")


def form(request):
    return render(request, "forms.html")


def card(request):
    return render(request, "cards.html")


def chart(request):
    return render(request, "charts.html")


def button(request):
    return render(request, "buttons.html")


def modal(request):
    return render(request, "modals.html")


def table(request):
    return render(request, "tables.html")


def deployment(request):
    context = {}
    user_id = request.session["userID"]
    user_role = request.session["role"]
    context.update(get_deployments(user_id, user_role))
    context.update(get_service_health(user_id, user_role))
    context.update(get_data_drift(user_id, user_role))
    context.update(get_accuracy(user_id, user_role))
    context.update(deployed_models(user_id, user_role))
    context.update(get_pending(user_id, user_role))
    return render(request, "deployments.html", context)


def overview(request, Project_Name):
    # if request.session["userID"] == model_id:
    context = {}
    user_id = request.session["userID"]
    context.update({'Project_Name': Project_Name})
    context.update(get_model(Project_Name))
    context.update(get_dataset(Project_Name))
    context.update(get_project(Project_Name))
    context.update(check_pending(Project_Name))
    return render(request, "overview.html", context)
    # return HttpResponseRedirect(reverse('overview', args=(model_id,)))


def approveModel(request, model_name):
    model_id = request.POST.get('model_id')
    project_name = request.POST.get('project_name')
    comments = request.POST.get('comments')
    approved_datetime = datetime.strftime(
        timezone.now(), '%Y-%m-%d %H:%M:%S%z')
    print(model_id)
    try:
        # change current champion to Challenger. Approve Status: Approved -> None
        if Model_List.objects.filter(Project_Name=project_name, Challenger_Status='Champion').exists():
            Model_List.objects.filter(Project_Name=project_name, Challenger_Status='Champion').update(
                 Challenger_Status='Challenger', Approve_Status='None')
        # change current pending to champion tgt with other columns
        Model_List.objects.filter(Model_id=model_id).update(
             Approve_Comments=comments, Challenger_Status='Champion',
             Approved_Date=approved_datetime, Approve_Status='Approved') 

        updated_model = Model_List.objects.get(Model_ID=model_id)
        # print the updated fields to the console
        print(
            f"Updated status: {updated_model.Model_ID}, {updated_model.Approve_Status}")
        print(
            f"Updated comments: {updated_model.Model_ID}, {updated_model.Approve_Comments}")
        return JsonResponse({'success': True})

    except Exception as e:
        print(e)
        return JsonResponse({'success': False})


def addModel(request, Project_Name):

    user_id = request.session["userID"]  # returns string
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT MAX(CAST("Model_ID" AS integer)) FROM core_model_list;')
        max_id = cursor.fetchone()[0]

    new_id = int(max_id) + 1
    model_name = request.POST.get('model_name')
    project_name = request.POST.get('project_name')
    description = request.POST.get('description')
    language = request.POST.get('language')
    version = request.POST.get('version')
    datasetId = request.POST.get('datasetId')
    current_datetime = datetime.strftime(timezone.now(), '%Y-%m-%d %H:%M:%S%z')

    Approve_User = Users.objects.get(pk='john@mlops.com')
    # for now, hardcode this. have to change to actual user id when login page is done.
    # user = Users.objects.get(pk='hannah@mlops.com')
    print(user_id)
    user = Users.objects.get(pk=user_id)
    datasetlist_ID = Dataset_List.objects.get(pk=datasetId)
    try:
        new_model = Model_List(
            Model_ID=new_id,
            Model_name=model_name,
            Model_version=version,
            Project_Name=project_name,
            Language=language,
            User_ID=user,
            Dataset_ID=datasetlist_ID,
            Model_description=description,
            Approve_Status='None',
            Approve_User_ID=Approve_User,
            Change_Comments='',
            Approve_Comments='',
            Created_Date=current_datetime,  # datetime field
            Approved_Date=None,  
            Service_Health_Status='Passing',
            Data_Drift_Status='Passing',
            Accuracy_Status='Passing',
            Challenger_Status='Challenger'
        )
        new_model.save()

        # create dates for the data
        timez = pytz.timezone('Asia/Singapore')
        dates = pd.date_range(start='4/6/2023', periods=5,tz=timez).normalize()
        print(dates)

        # create a dataframe with the columns
        data = pd.DataFrame({'Date': dates})

        # generate random data for each column
        data['AUC'] = np.random.normal(loc=0.77, scale=0.001, size=len(dates))
        data['KS'] = np.random.normal(loc=0.6, scale=0.1, size=len(dates))
        data['LogLoss'] = np.random.normal(
            loc=0.65, scale=0.01, size=len(dates))
        data['Gini_NormI'] = np.random.normal(
            loc=0.2, scale=0.01, size=len(dates))
        data['Rate_Top10'] = np.random.normal(
            loc=0.9, scale=0.01, size=len(dates))
        data['Location'] = "West"

        # create the other data frames with different locations
        data_north = data.copy()
        data_north['Location'] = "North"

        data_east = data.copy()
        data_east['Location'] = "East"

        data_south = data.copy()
        data_south['Location'] = "South"

        # concatenate all data frames together
        all_data = pd.concat(
            [data, data_north, data_east, data_south], ignore_index=True)

        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT MAX("id") FROM core_model_accuracy;')
            max_accuracy_id = cursor.fetchone()[0]
        print(max_accuracy_id)

        for i in range(len(all_data)):
            new_accuracy = Model_Accuracy(
                id=max_accuracy_id + i + 1,
                LogLoss=all_data['LogLoss'][i],
                AUC=all_data['AUC'][i],
                KS=all_data['KS'][i],
                Gini_Norm=all_data['Gini_NormI'][i],
                Rate_Top10=all_data['Rate_Top10'][i],
                Date=all_data['Date'][i],
                Location=all_data['Location'][i],
                Target=50,
                Predicted=50,
                Model_ID=new_model,
                Dataset_ID=datasetlist_ID
            )
            new_accuracy.save()
        return JsonResponse({'success': True})
    except Exception as e:
        print("exception", e)
        return JsonResponse({'success': False})


def accuracy(request, Project_Name):
    context = {}
    user_id = request.session["userID"]
    context.update({'Project_Name': Project_Name})
    return render(request, "accuracy.html", context)


def accuracy_chart(request, Project_Name):
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    metric = request.GET.get('metric', None)
    resolution = request.GET.get('resolution', None)
    location = request.GET.get('location', None)
    if resolution == 'Select':
        resolution = None
    if location == 'Select':
        location = None

    query_dict = {
        'Daily': 'SELECT "Date", AVG("{}") as "{}" FROM core_model_accuracy WHERE "Model_ID_id" = \'{}\' AND "Date" BETWEEN %s AND %s {} GROUP BY "Date" ORDER BY "Date"',
        'Weekly': 'SELECT date_trunc(\'week\', "Date") as "Date", AVG("{}") as "{}" FROM core_model_accuracy WHERE "Date" BETWEEN %s AND %s {} GROUP BY date_trunc(\'week\', "Date") ORDER BY "Date"',
        'Monthly': 'SELECT date_trunc(\'month\', "Date") as "Date", AVG("{}") as "{}" FROM core_model_accuracy WHERE "Date" BETWEEN %s AND %s {} GROUP BY date_trunc(\'month\', "Date") ORDER BY "Date"'
    }

    # Get earliest and latest date from database
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT MIN("Date"), MAX("Date") FROM core_model_accuracy')
        min_date, max_date = cursor.fetchone()

        cursor.execute(
            'select "Model_ID" from core_model_list where "Challenger_Status" = \'Champion\' and "Project_Name"=\'{}\''.format(Project_Name))
        model_id = cursor.fetchone()[0]
        # model_id = 1005

        if not start_date:
            start_date = min_date
        if not end_date:
            end_date = max_date
        if resolution:
            # Get the appropriate SQL query based on the selected resolution
            query = query_dict[resolution].format(
                metric, metric, model_id, "AND \"Location\" = '{}'".format(location) if location else "")
            cursor.execute(query, [start_date, end_date])
            data = cursor.fetchall()
        else:
            query = query_dict['Daily'].format(
                metric, metric, model_id, "AND \"Location\" = '{}'".format(location) if location else "")
            cursor.execute(query, [start_date, end_date])
            data = cursor.fetchall()

    column_data = []
    date_labels = []
    for row in data:
        date_labels.append(row[0])
        column_data.append(row[1])
    chart_data = {
        'title': "{} over time".format(metric),
        'data': {
            "labels": date_labels,
            "datasets": [
                {
                    "label": "{} over time".format(metric),
                    "data": column_data,
                    "fill": False,
                    "borderColor": "rgb(75, 192, 192)",
                    "lineTension": 0.1
                }
            ]
        }
    }
    return JsonResponse(chart_data)


def service_health(request, Project_Name):
    context = {}
    user_id = request.session["userID"]
    context.update({'Project_Name': Project_Name})
    return render(request, "service_health.html", context)


def service_chart(request, Project_Name):
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    metric = request.GET.get('metric', None)
    resolution = request.GET.get('resolution', None)
    location = request.GET.get('location', None)
    if resolution == 'Select':
        resolution = None
    if location == 'Select':
        location = None

    query_dict = {
        'Daily': 'SELECT "Date", AVG("{}") as "{}" FROM core_service_health WHERE "Model_ID_id" = \'{}\' AND "Date" BETWEEN %s AND %s {} GROUP BY "Date" ORDER BY "Date"',
        'Weekly': 'SELECT date_trunc(\'week\', "Date") as "Date", AVG("{}") as "{}" FROM core_service_health WHERE "Date" BETWEEN %s AND %s {} GROUP BY date_trunc(\'week\', "Date") ORDER BY "Date"',
        'Monthly': 'SELECT date_trunc(\'month\', "Date") as "Date", AVG("{}") as "{}" FROM core_service_health WHERE "Date" BETWEEN %s AND %s {} GROUP BY date_trunc(\'month\', "Date") ORDER BY "Date"'
    }

    # Get earliest and latest date from database
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT MIN("Date"), MAX("Date") FROM core_service_health')
        min_date, max_date = cursor.fetchone()

        cursor.execute(
            'select "Model_ID" from core_model_list where "Challenger_Status" = \'Champion\' and "Project_Name"=\'{}\''.format(Project_Name))
        model_id = cursor.fetchone()[0]
        # model_id = 1005

        if not start_date:
            start_date = min_date
        if not end_date:
            end_date = max_date
        if resolution:
            # Get the appropriate SQL query based on the selected resolution
            query = query_dict[resolution].format(
                metric, metric, model_id, "AND \"Location\" = '{}'".format(location) if location else "")
            cursor.execute(query, [start_date, end_date])
            data = cursor.fetchall()
        else:
            query = query_dict['Daily'].format(
                metric, metric, model_id, "AND \"Location\" = '{}'".format(location) if location else "")
            cursor.execute(query, [start_date, end_date])
            data = cursor.fetchall()

    column_data = []
    date_labels = []
    for row in data:
        date_labels.append(row[0])
        column_data.append(row[1])
    chart_data = {
        'title': "{} over time".format(metric),
        'data': {
            "labels": date_labels,
            "datasets": [
                {
                    "label": "{} over time".format(metric),
                    "data": column_data,
                    "fill": False,
                    "borderColor": "rgb(75, 192, 192)",
                    "lineTension": 0.1
                }
            ]
        }
    }
    return JsonResponse(chart_data)


def challenger_chart(request, Project_Name):
    # Get earliest and latest date from database
    metric = request.GET.get('metric', "AUC")
    print(metric)
    with connection.cursor() as cursor:
        query = 'SELECT "Date", "Model_ID_id", AVG("{}") FROM core_model_accuracy GROUP BY "Date", "Model_ID_id" ORDER BY "Date", "Model_ID_id"'.format(
            metric)
        cursor.execute(query)
        data = cursor.fetchall()

    model_data = {}
    date_labels = []
    for row in data:
        date = row[0]
        model_id = row[1]
        auc = row[2]

        if model_id not in model_data:
            model_data[model_id] = {
                'label': 'Model {}'.format(model_id), 'data': []}

        model_data[model_id]['data'].append(auc)

        if date not in date_labels:
            date_labels.append(date)

    datasets = []
    for model_id, data in model_data.items():
        datasets.append({
            'label': data['label'],
            'data': data['data'],
            'fill': False,
            'lineTension': 0.1
        })

    chart_data = {
        'title': 'AUC over time for different models',
        'data': {
            'labels': date_labels,
            'datasets': datasets
        }
    }

    return JsonResponse(chart_data)


def datadrift(request, Project_Name):
    context = {}
    user_id = request.session["userID"]
    context.update({'Project_Name': Project_Name})
    context.update(drift_importance(Project_Name))
    context.update(feature_distribution(Project_Name))

    if request.method == 'POST':
        if request.POST['form_id'] == 'chart_change':
            start_date = request.POST['start_time_option']
            end_date = request.POST['end_time_option']
            context.update(drift_importance(
                Project_Name, start_date, end_date))
            context.update(feature_distribution(
                Project_Name, start_date, end_date))
            return JsonResponse(context)

    return render(request, "datadrift.html", context)


def challengers(request, Project_Name):
    context = {}
    user_id = request.session["userID"]
    context.update({'Project_Name': Project_Name})
    context.update(get_registry_models(user_id, Project_Name))
    context.update(get_registry_count(user_id, Project_Name))
    return render(request, "challengers.html", context)

def get_dataset_info(request, Project_Name):
    print(Project_Name)
    # if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
    Dataset_id = request.GET.get('dataset_id')
    dataset = get_object_or_404(Dataset_List, pk=Dataset_id)
    dataset_list = {
        'Dataset_name': dataset.Dataset_name,
        'num_of_rows': dataset.num_of_rows,
        'num_of_features': dataset.num_of_features,
        'Target': dataset.Target,
    }
    return JsonResponse(dataset_list)



def modelRegistry(request, Project_Name):
    dataset_list = Dataset_List.objects.all()
    # project_name = Model_List.objects.values('Project_Name').distinct()
    # If the request accepts JSON, return a JSON response
    if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
        Dataset_id = request.GET.get('dataset_id')
        dataset = get_object_or_404(Dataset_List, pk=Dataset_id)
        dataset_list = {
            'Dataset_name': dataset.Dataset_name,
            'num_of_rows': dataset.num_of_rows,
            'num_of_features': dataset.num_of_features,
            'Target': dataset.Target,
        }
        return JsonResponse(dataset_list)

    # Otherwise, return the HTML page
    return render(request, "modelRegistry.html", {'dataset_list': dataset_list, 'Project_Name': Project_Name})


def humility(request, Project_Name):
    context = {}
    user_id = request.session["userID"]
    context.update({'Project_Name': Project_Name})
    return render(request, "humility.html", context)


def humility_add(request, Project_Name):
    context = {}
    user_id = request.session["userID"]
    context.update({'Project_Name': Project_Name})
    return render(request, "humilityAdd.html", context)

# def mregistry(request):
#     return render(request, "mregistry.html")


def loginpage(request):
    return render(request, "loginpage.html")


def codeEditor2(request):
    return render(request, "codeEditor2.html")

def run_code(request):
    if request.method == "POST":
        print('in post')
        # Get the selected programming language and code from the form data
        lang = request.POST.get("lang")
        code = request.POST.get("code")
        command = ''
        # Choose the appropriate interpreter or compiler based on the selected language
        if lang == "python":
            command = ["python", "-c", code]
        elif lang == "javascript":
            command = ["node", "-e", code]

        elif lang == "c":
            filename = "program.c"
            with open(filename, "w") as f:
                f.write(code)
            print(f'f: {f}')
            print(f'filename: {filename}')
            command = ["gcc", filename, "-o", "program"]
            try:
                subprocess.run(command, check=True)
                print("Compilation successful")
                command = ["./program"]
            except subprocess.CalledProcessError as e:
                print("Compilation failed: ", e)

        elif lang == "cpp":
            filename = "program.cpp"
            with open(filename, "w") as f:
                f.write(code)

            command = ["g++", filename, "-o", "program"]
            try:
                subprocess.run(command, check=True)
                print("Compilation successful")
                command = ["./program"]
            except subprocess.CalledProcessError as e:
                print("Compilation failed: ", e)

        print('after  allocating')
        try:
            # Run the command using subprocess and capture the output
            # result = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=False, timeout=10, universal_newlines=True)
            process = subprocess.Popen(
                command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = process.communicate(input='')
            result = stdout + stderr
            response_data = {"success": True, "result": result}
        except subprocess.CalledProcessError as e:
            response_data = {"success": False, "error": str(e.output)}
        except subprocess.TimeoutExpired as e:
            response_data = {"success": False, "error": "Time limit exceeded"}
        except Exception as e:
            response_data = {"success": False, "error": str(e)}
        return JsonResponse(response_data)


def homepage(request):
    return HttpResponse("Hello, world. The dashboard is under construction. Try ../app/main/")


def handler404(request):
    response = render(request, 'index.html')
    response.status_code = 404
    return response


# CODE PORTING
# import js2py
# import pybind11 # Python to cpp


def translate_code(request, Project_Name):
    if request.method == 'POST':
        translate_from = request.POST['portFromLanguage']
        translate_to = request.POST['portToLanguage']
        code_translate_from = request.POST['codeTranslateFrom']

        try:
            if translate_from == 'python' and translate_to == 'javascript':  # NOT HARD CODED
                '''Test case:
                ```
                for i in range(5):
                    print(i)
                ```
                '''
                code_translate_to = pscript.py2js(code_translate_from)

            elif translate_from == 'javascript' and translate_to == 'python':
                # code_translate_to = js2py.translate_js(code_translate_from)
                '''hard code:
                ```
                var i;
                for (i = 0; i < 5; i += 1) {
                    console.log(i);
                }
                ```
                '''
                code_translate_from_formatted = re.sub(
                    r"[\n\t\s]*", "", code_translate_from)
                # print(code_translate_from_formatted)

                if code_translate_from_formatted != "vari;for(i=0;i<5;i+=1){console.log(i);}":
                    code_translate_to = "ERROR: Try again with a different code snippet. This code snippet is not supported."
                else:
                    code_translate_to = "for i in range(5):\n    print(i)"

            elif translate_from == 'python' and translate_to == 'cpp':
                '''hard code:
                ```
                for i in range(5):
                    print(i)
                ```
                '''
                code_translate_from_formatted = re.sub(
                    r"[\n\t\s]*", "", code_translate_from)
                # if code_translate_from_formatted != "vari;for(i=0;i<5;i+=1){console.log(i);}":
                if code_translate_from_formatted != "foriinrange(5):print(i)":
                    code_translate_to = "ERROR: Try again with a different code snippet. This code snippet is not supported."
                else:
                    code_translate_to = "#include <iostream>\nusing namespace std;\n\nint main() {\n  for (int i = 0; i < 5; i++) {\n    cout << i << endl;\n  }\n  return 0;\n}"

            elif translate_from == 'cpp' and translate_to == 'python':
                '''
                hard code:
                ```
                #include <iostream>
                using namespace std;

                int main() {
                    for (int i = 0; i < 5; i++) {
                        cout << i << endl;
                    }
                    return 0;
                }
                ```
                '''
                code_translate_from_formatted = re.sub(
                    r"[\n\t\s]*", "", code_translate_from)
                if code_translate_from_formatted != "#include<iostream>usingnamespacestd;intmain(){for(inti=0;i<5;i++){cout<<i<<endl;}return0;}":
                    code_translate_to = "ERROR: Try again with a different code snippet. This code snippet is not supported."
                else:
                    code_translate_to = "for i in range(5):\n    print(i)"

            elif translate_from == 'python' and translate_to == 'c':
                '''hard code:
                ```
                for i in range(5):
                    print(i)
                ```
                '''
                code_translate_from_formatted = re.sub(
                    r"[\n\t\s]*", "", code_translate_from)
                # if code_translate_from_formatted != "vari;for(i=0;i<5;i+=1){console.log(i);}":
                if code_translate_from_formatted != "foriinrange(5):print(i)":
                    code_translate_to = "ERROR: Try again with a different code snippet. This code snippet is not supported."
                else:
                    code_translate_to = "#include <stdio.h>\n\nint main() {\n    int i;\n    for (i = 0; i < 5; i++) {\n        printf(\"%d\\n\", i);\n    }\n    return 0;\n}"

            elif translate_from == 'c' and translate_to == 'python':
                '''hard code:
                ```
                #include <stdio.h>

                int main() {
                    printf("Hello World!");
                    return 0;
                }
                ```
                '''
                code_translate_from_formatted = re.sub(
                    r"[\n\t\s]*", "", code_translate_from)
                # code_translate_from_formatted = code_translate_from_formatted.rstrip('%')
                print(code_translate_from_formatted)
                if code_translate_from_formatted != '#include<stdio.h>intmain(){printf("HelloWorld!");return0;}':
                    code_translate_to = "ERROR: Try again with a different code snippet. This code snippet is not supported."
                else:
                    code_translate_to = 'print("Hello World!")'

            elif translate_from == 'javascript' and translate_to == 'cpp':
                '''hard code:
                ```
                var i;
                for (i = 0; i < 5; i += 1) {
                    console.log(i);
                }
                ```
                '''
                code_translate_from_formatted = re.sub(
                    r"[\n\t\s]*", "", code_translate_from)

                if code_translate_from_formatted != "vari;for(i=0;i<5;i+=1){console.log(i);}":
                    code_translate_to = "ERROR: Try again with a different code snippet. This code snippet is not supported."
                else:
                    code_translate_to = "#include <iostream>\nusing namespace std;\n\nint main() {\n  for (int i = 0; i < 5; i += 1) {\n    cout << i << endl;\n  }\n  return 0;\n}"

            elif translate_from == 'cpp' and translate_to == 'javascript':
                '''hard code:
                ```
                #include <iostream>
                using namespace std;

                int main() {
                    for (int i = 0; i < 5; i++) {
                        cout << i << endl;
                    }
                    return 0;
                }
                ```
                '''
                code_translate_from_formatted = re.sub(
                    r"[\n\t\s]*", "", code_translate_from)
                if code_translate_from_formatted != "#include<iostream>usingnamespacestd;intmain(){for(inti=0;i<5;i++){cout<<i<<endl;}return0;}":
                    code_translate_to = "ERROR: Try again with a different code snippet. This code snippet is not supported."
                else:
                    code_translate_to = "var i;\nfor (i = 0; i < 5; i += 1) {\n  console.log(i);\n}"

            else:
                return JsonResponse({'error': 'Language combination still WIP.'})

            return JsonResponse({'translated_code': code_translate_to})
        except:
            return JsonResponse({'error': 'Translation error'})

    else:
        return render(request, 'modelRegistry.html')


# CODE EDITOR
def save_saved(request, Project_Name):
    if request.method == 'POST':
        code = request.POST['code']
        lang = request.POST['filechooser']
        filename = request.POST['fileName']

        _filename = f'{filename}.{lang}'
        with open(_filename, 'w') as fp:
            fp.write(code)
            fp.close()
            print(f'saved as {_filename}')
        messages.success(request, f"Successfully saved file {_filename}.")
        return redirect(reverse("modelRegistry", Project_Name))


# retrieve data information from the database, when user select data to test model
# def get_dataset_info(request):
#   dataset_id = request.GET.get("dataset_id")
#   dataset = Model_Accuracy.objects.filter(Model_ID=dataset_id).first()
#   data = {
#     "dataset_name": dataset.Model_name,
#     "num_rows": dataset.num_rows,
#     "num_features": dataset.num_features
#   }
#   return JsonResponse(data)

# LOGIN Functions
def userlogin(request):
    msg = ''
    context = {}
    if request.method == 'POST':
        username = request.POST.get("email")
        pwd = request.POST.get("password")
        user = Users.objects.filter(User_ID=username, Password=pwd).count()
        if user == 1:
            print(username)
            user = Users.objects.filter(User_ID=username, Password=pwd).first()
            request.session["userLogin"] = True
            request.session["userID"] = user.User_ID
            if user.Role == "MLOps Engineer":
                request.session["role"] = 'MLOps Engineer'
            else:
                request.session["role"] = "Data Scientist"
            # return redirect('/app/deployment')
            context.update(get_deployments(user.User_ID, user.Role))
            context.update(get_service_health(user.User_ID, user.Role))
            context.update(get_data_drift(user.User_ID, user.Role))
            context.update(get_accuracy(user.User_ID, user.Role))
            context.update(deployed_models(user.User_ID, user.Role))
            # return redirect('/app/deployment')
            return redirect(reverse("deployment"))
            # return render(request, 'deployments.html', context = context)
            # msg = 'Success'
        else:
            msg = 'Invalid Email/Password'
    # form = forms.UserLoginForm
    return render(request, 'loginpage.html', {'msg': msg})


def userlogout(request):
    if request.method == "GET":
        request.session.flush()
    # return redirect('/app/logout')
    # if (request.GET.get("logoutbtn")):
        # del request.session["userLogin"]
        return render(request, 'logoutpage.html')


def make_champion_model(request, Project_Name):
    new_cham_model_id = request.POST.get('model_id')
    comments = request.POST.get('comments')
    approved_datetime = datetime.strftime(timezone.now(), '%Y-%m-%d %H:%M:%S%z')
    try:
        Model_List.objects.filter(Model_ID=new_cham_model_id).update(
            Approve_Status='Pending', Change_Comments=comments)

        return JsonResponse({'success': True})
    except Exception as e:
        print(e)
        return JsonResponse({'success': False})

    
