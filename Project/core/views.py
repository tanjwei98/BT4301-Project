from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import *

# from models import Model_Accuracy

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
    return render(request, "deployments.html")

def overview(request):
    return render(request, "overview.html")

def accuracy(request):
    return render(request, "accuracy.html")

def service_health(request):
    return render(request, "service_health.html")

def datadrift(request):
    return render(request, "datadrift.html")
    
def challengers(request):
    return render(request, "challengers.html")

def modelRegistry(request):
    dataset_list = Dataset_List.objects.all()
    print(request.META.get('HTTP_ACCEPT'))
    # If the request accepts JSON, return a JSON response
    if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
        
        Dataset_id = request.GET.get('dataset_id')
        print(Dataset_id)
        dataset = get_object_or_404(Dataset_List, pk=Dataset_id)
        print('in here')
        print('in the rendering page')
        dataset_list = {
            'Dataset_name': dataset.Dataset_name,
            'num_of_rows': dataset.num_of_rows,
            'num_of_features': dataset.num_of_features,
        }
        return JsonResponse(dataset_list)

    # Otherwise, return the HTML page
    return render(request, "modelRegistry.html", {'dataset_list': dataset_list})




def humility(request):
    return render(request, "humility.html")

def humility_add(request):
    return render(request, "humilityAdd.html")

# def mregistry(request):
#     return render(request, "mregistry.html")

def loginpage(request):
    return render(request, "loginpage.html")

def homepage(request):
    return HttpResponse("Hello, world. The dashboard is under construction. Try ../app/main/")

def handler404(request):
    response = render(request, 'index.html')
    response.status_code = 404
    return response


# CODE PORTING 
import pscript
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
                code_translate_to = "for i in range(5):\n    print(i)"

            elif translate_from == 'python' and translate_to == 'cpp':  
                '''hard code: 
                ```
                for i in range(5): 
                    print(i)
                ```
                '''
                code_translate_to = "#include <iostream>\nusing namespace std;\n\nint main() {\n  for (int i = 0; i < 5; i++) {\n    cout << i << endl;\n  }\n  return 0;\n}"

            elif translate_from == 'cpp' and translate_to == 'python':  
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
               code_translate_to = "for i in range(5):\n    print(i)"

            elif translate_from == 'python' and translate_to == 'c':  
                '''hard code: 
                ```
                for i in range(5): 
                    print(i)
                ```
                '''
                code_translate_to = "#include <stdio.h>\n\nint main() {\n    int i;\n    for (i = 0; i < 5; i++) {\n        printf(\"%d\\n\", i);\n    }\n    return 0;\n}"

            elif translate_from == 'c' and translate_to == 'python':  
               '''hard code: 
                ```
                #include <stdio.h>

                int main() {
                    int i;
                    for (i = 0; i < 5; i++) {
                        printf("%d\n", i);
                    }
                    return 0;
                }
                ```
                '''
               code_translate_to = "for i in range(5):\n    print(i)"

            elif translate_from == 'javascript' and translate_to == 'cpp':  
                '''hard code: 
                ```
                var i;
                for (i = 0; i < 5; i += 1) {
                    console.log(i);
                }
                ```
                '''
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
               code_translate_to = "var i;\nfor (i = 0; i < 5; i += 1) {\n  console.log(i);\n}"

            else: 
                return JsonResponse({'error':'Language combination still WIP.'})

            return JsonResponse({'translated_code': code_translate_to})
        except:
            return JsonResponse({'error':'Translation error'})

    else:
        return render(request, 'modelRegistry.html')
    
from pathlib import Path  
from os import path
from rest_framework.decorators import api_view


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
    if request.method=='POST':
        username = request.POST.get("email")
        pwd = request.POST.get("password")
        user = Users.objects.filter(User_ID = username, Password = pwd).count()
        if user == 1:
            user = Users.objects.filter(User_ID = username, Password = pwd).first()
            request.session["userLogin"]= True
            request.session["userID"] = user.User_ID
            if user.Role == "MLOps Engineer":
                request.session["role"] = 'MLOps Engineer'
            else:
                request.session["role"] = "Data Scientist"
            return redirect('/app/deployment')
            # msg = 'Success'
        else:
            msg = 'Invalid Email/Password'
    #form = forms.UserLoginForm
    return render(request, 'loginpage.html',{'msg':msg})

def userlogout(request):
    del request.session["userLogin"]
    redirect('/app/login')

