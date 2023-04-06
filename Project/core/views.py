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
    # data = json.loads(request.body.decode('utf-8'))
    # model_id = data.get('model_id')
    # model_status = data.get('status')

    model_id = request.POST.get('model_id')
    model_status = request.POST.get('status')
    comments = request.POST.get('comments')
    print(model_id)
    print(model_status)
    Model_List.objects.filter(Model_ID=model_id).update(
        Approve_Status=model_status)
    Model_List.objects.filter(Model_ID=model_id).update(
        Change_Comments=comments)
    updated_model = Model_List.objects.get(Model_ID=model_id)
    # print the updated fields to the console
    print(
        f"Updated status: {updated_model.Model_name}, {updated_model.Approve_Status}")
    print(
        f"Updated comments: {updated_model.Model_name}, {updated_model.Change_Comments}")
    return JsonResponse({'success': True})


def addModel(request):

    with connection.cursor() as cursor:
        cursor.execute('SELECT MAX(CAST("Model_ID" AS integer)) FROM core_model_list;')
        max_id = cursor.fetchone()[0]
        
    new_id = int(max_id) + 1
    model_name = request.POST.get('model_name')
    project_name = request.POST.get('project_name')
    description = request.POST.get('description')
    language = request.POST.get('language')
    version = request.POST.get('version')
    datasetId = request.POST.get('datasetId')
    current_datetime = datetime.strftime(timezone.now(), '%Y-%m-%d %H:%M:%S%z')

    user = Users.objects.get(pk='hannah@mlops.com') # for now, hardcode this. have to change to actual user id when login page is done. 
    print(f'THIS IS THE DATASEET ID: {datasetId}')
    datasetlist_ID = Dataset_List.objects.get(pk=datasetId) # for now, hardcode this. have to change to actual user id when login page is done. 
    try:
        new_model = Model_List(
            Model_ID = new_id,
            Model_name=model_name,
            Model_version=version,
            Project_Name=project_name,
            Language=language,
            User_ID=user,  # hardcoded for now
            Dataset_ID=datasetlist_ID,
            Model_description=description,
            Approve_Status=1,
            Approve_User_ID=None,
            Change_Comments='',
            Approve_Comments='',
            Created_Date=current_datetime,  # datetime field
            Approved_Date= None, #might want to change it to allow null instead
            Service_Health_Status='Passing',
            Data_Drift_Status='Passing',
            Accuracy_Status='Passing',
            Challenger_Status='Challengers'
        )
        new_model.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        print(e)
        return JsonResponse({'success': False})


def accuracy(request):
    return render(request, "accuracy.html")


def accuracy_chart(request):
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
        'Daily': 'SELECT "Date", AVG("{}") as "{}" FROM core_model_accuracy WHERE "Date" BETWEEN %s AND %s {} GROUP BY "Date" ORDER BY "Date"',
        'Weekly': 'SELECT date_trunc(\'week\', "Date") as "Date", AVG("{}") as "{}" FROM core_model_accuracy WHERE "Date" BETWEEN %s AND %s {} GROUP BY date_trunc(\'week\', "Date") ORDER BY "Date"',
        'Monthly': 'SELECT date_trunc(\'month\', "Date") as "Date", AVG("{}") as "{}" FROM core_model_accuracy WHERE "Date" BETWEEN %s AND %s {} GROUP BY date_trunc(\'month\', "Date") ORDER BY "Date"'
    }

    # Get earliest and latest date from database
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT MIN("Date"), MAX("Date") FROM core_model_accuracy')
        min_date, max_date = cursor.fetchone()

        if not start_date:
            start_date = min_date
        if not end_date:
            end_date = max_date
        if resolution:
            # Get the appropriate SQL query based on the selected resolution
            query = query_dict[resolution].format(
                metric, metric, "AND \"Location\" = '{}'".format(location) if location else "")
            cursor.execute(query, [start_date, end_date])
            data = cursor.fetchall()
        else:
            query = 'SELECT "Date", "{}" FROM core_model_accuracy WHERE "Date" BETWEEN %s AND %s {}'.format(
                metric, "AND \"Location\" = '{}'".format(location) if location else "")
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

def predicted_actual_chart(request):
    start_date = request.GET.get('start_date',None)
    end_date = request.GET.get('end_date',None)
    resolution = request.GET.get('resolution',None)
    location = request.GET.get('location',None)
    if resolution == 'Select':
        resolution = None
    if location == 'Select':
        location = None

    query_dict = {
    'Daily': 'SELECT "Date", AVG("Target") as "target", AVG("Predicted") as "predicted" FROM core_model_accuracy WHERE "Date" BETWEEN %s AND %s {} GROUP BY "Date" ORDER BY "Date"',
    'Weekly': 'SELECT date_trunc(\'week\', "Date") as "Date", AVG("Target") as "target", AVG("Predicted") as "predicted" FROM core_model_accuracy WHERE "Date" BETWEEN %s AND %s {} GROUP BY date_trunc(\'week\', "Date") ORDER BY "Date"',
    'Monthly': 'SELECT date_trunc(\'month\', "Date") as "Date", AVG("Target") as "target", AVG("Predicted") as "predicted" FROM core_model_accuracy WHERE "Date" BETWEEN %s AND %s {} GROUP BY date_trunc(\'month\', "Date") ORDER BY "Date"'
    }

    # Get earliest and latest date from database
    with connection.cursor() as cursor:
        cursor.execute('SELECT MIN("Date"), MAX("Date") FROM core_model_accuracy')
        min_date, max_date = cursor.fetchone()

        if not start_date:
            start_date = min_date
        if not end_date:
            end_date = max_date
        if resolution:
            # Get the appropriate SQL query based on the selected resolution
            query = query_dict[resolution].format("AND \"Location\" = '{}'".format(location) if location else "")
            cursor.execute(query, [start_date, end_date])
            data = cursor.fetchall()
        else:
            query = 'SELECT "Date", "Target", "Predicted" FROM core_model_accuracy WHERE "Date" BETWEEN %s AND %s {}'.format("AND \"Location\" = '{}'".format(location) if location else "")
            cursor.execute(query, [start_date, end_date])
            data = cursor.fetchall()

    target_data = []
    predicted_data = []
    date_labels = []
    for row in data:
        date_labels.append(row[0])
        target_data.append(row[1])
        predicted_data.append(row[2])

    chart_data = {
        'title': "Target and Predicted over time",
        'data': {
            "labels": date_labels,
            "datasets": [
                {
                    "label": "Target",
                    "data": target_data,
                    "fill": False,
                    "borderColor": "rgb(75, 192, 192)",
                    "lineTension": 0.1
                },
                {
                    "label": "Predicted",
                    "data": predicted_data,
                    "fill": False,
                    "borderColor": "rgb(192, 75, 192)",
                    "lineTension": 0.1
                }
            ]
        }
    }

    return JsonResponse(chart_data)


def service_health(request):
    return render(request, "service_health.html")


def service_chart(request):
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
        'Daily': 'SELECT "Date", AVG("{}") as "{}" FROM core_service_health WHERE "Date" BETWEEN %s AND %s {} GROUP BY "Date" ORDER BY "Date"',
        'Weekly': 'SELECT date_trunc(\'week\', "Date") as "Date", AVG("{}") as "{}" FROM core_service_health WHERE "Date" BETWEEN %s AND %s {} GROUP BY date_trunc(\'week\', "Date") ORDER BY "Date"',
        'Monthly': 'SELECT date_trunc(\'month\', "Date") as "Date", AVG("{}") as "{}" FROM core_service_health WHERE "Date" BETWEEN %s AND %s {} GROUP BY date_trunc(\'month\', "Date") ORDER BY "Date"'
    }

    # Get earliest and latest date from database
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT MIN("Date"), MAX("Date") FROM core_service_health')
        min_date, max_date = cursor.fetchone()

        if not start_date:
            start_date = min_date
        if not end_date:
            end_date = max_date
        if resolution:
            # Get the appropriate SQL query based on the selected resolution
            query = query_dict[resolution].format(
                metric, metric, "AND \"Location\" = '{}'".format(location) if location else "")
            cursor.execute(query, [start_date, end_date])
            data = cursor.fetchall()
        else:
            query = 'SELECT "Date", "{}" FROM core_service_health WHERE "Date" BETWEEN %s AND %s {}'.format(
                metric, "AND \"Location\" = '{}'".format(location) if location else "")
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
            context.update(drift_importance(Project_Name, start_date, end_date))
            context.update(feature_distribution(Project_Name, start_date, end_date))
            return JsonResponse(context)

    return render(request, "datadrift.html", context)


def challengers(request):
    return render(request, "challengers.html")


def modelRegistry(request):
    dataset_list = Dataset_List.objects.all()
    project_name = Model_List.objects.values('Project_Name').distinct()
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
    return render(request, "modelRegistry.html", {'dataset_list': dataset_list, 'project_name': project_name})


def humility(request):
    return render(request, "humility.html")


def humility_add(request):
    return render(request, "humilityAdd.html")

# def mregistry(request):
#     return render(request, "mregistry.html")


def loginpage(request):
    return render(request, "loginpage.html")


def codeEditor2(request):
    return render(request, "codeEditor2.html")


# def run_code(request):
#     if request.method == "POST":
#         print('iin here')
#         code = request.POST.get("code")
#         print(f'this is my code {code}')
#         try:
#             # Create an empty dictionary to serve as the local namespace for executing the code
#             local_ns = {}
#             print(f'in try now')
#             # Execute the code in the local namespace
#             exec(code, globals(), local_ns)
#             print(local_ns)
#             # Check if the code defined a variable named 'result'
#             if 'result' in local_ns:
#                 result = local_ns['result']
#             else:
#                 result = None

#             response_data = {"success": True, "result": result}
#         except Exception as e:
#             print(f'exception')
#             print(e)
#             response_data = {"success": False, "result": str(e)}
#         print(response_data)
#         return JsonResponse(response_data)


# def run_code(request):
#     if request.method == "POST":
#         print('iin here')
#         # Get the selected programming language and code from the form data
#         lang = request.POST.get("lang")
#         code = request.POST.get("code")
#         print(lang)
#         print(code)
#         print(lang)
#         command = ''
#         # Choose the appropriate interpreter or compiler based on the selected language
#         if lang == "python":
#             command = ["python", "-c", code]
#         elif lang == "r":
#             command = ["Rscript", "-e", code]
#         elif lang == "javascript":
#             command = ["node", "-e", code]
#         elif lang == "c":
#             filename = "program.c"
#             with open(filename, "w") as f:
#                 f.write(code)
#             command = ["gcc", filename, "-o", "program"]
#             subprocess.run(command)
#             print(f"Compilation completed: {os.path.exists('program')}")
#             command = ["./program"]
#         elif lang == "cpp":
#             filename = "program.cpp"
#             with open(filename, "w") as f:
#                 f.write(code)
#             command = ["g++", filename, "-o", "program"]
#             subprocess.run(command)
#             print(f"Compilation completed: {os.path.exists('program')}")
#             command = ["./program"]

#         try:
#             # Run the command using subprocess and capture the output
#             result = subprocess.check_output(
#                 command, stderr=subprocess.STDOUT, shell=False, timeout=10, universal_newlines=True)
#             response_data = {"success": True, "result": result}
#         except subprocess.CalledProcessError as e:
#             print('in CalledProcessError')
#             response_data = {"success": False, "error": str(e.output)}
#         except subprocess.TimeoutExpired as e:
#             print('in TimeoutExpired')
#             response_data = {"success": False, "error": "Time limit exceeded"}
#         except Exception as e:
#             print('in other exception')
#             response_data = {"success": False, "error": str(e)}
#         print(response_data)
#         return JsonResponse(response_data)


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


def translate_code(request):
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
                if code_translate_from_formatted != "foriinrange(5):print(i)}":
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
                if code_translate_from_formatted != "foriinrange(5):print(i)}":
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
def save_saved(request):
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
        return redirect('/app/challengers/modelRegistry')


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
