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

def translate_code(request):
    if request.method == 'POST':
        translate_from = request.POST['portFromLanguage']
        translate_to = request.POST['portToLanguage']
        code_translate_from = request.POST['codeTranslateFrom']

        try: 
            if translate_from == 'python' and translate_to == 'javascript':  # OK 
                code_translate_to = pscript.py2js(code_translate_from)
            elif translate_from == 'javascript' and translate_to == 'python':  # WIP
                # code_translate_to = js2py.translate_js(code_translate_from)
                pass
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

# MODEL-RELATED.
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import pandas as pd


# from .serializers import *


# def refresh_all_data(request, version, format=None):
#     '''
#     Helper function to add our base test dataset to our postgresql
#     '''

#     '''Model info'''
#     df = pd.read_csv(os.path.join(os.getcwd(), "data/test_data.csv"))

#     # PROCESS DATA TO CORRECT FORMAT HERE


#     _ = update_database_records(df, models.ModelList)

#     return Response(status=status.HTTP_200_OK)  



# def update_database_records(df, db_class, *additional_composite_key_col):
#     '''
#     Takes in a dataframe (each column name aligned to a DB table's column name)
#     and perform an update to the associated Database Table
#     (only delete and recreating rows with updated information)
#     '''
#     datetime_col = [col for col in df.columns if df[col].dtype == 'datetime64[ns, UTC]']

#     pk_col = db_class._meta.pk.name
#     foreign_keys = [field for field in db_class._meta.fields if (field.many_to_one or field.one_to_one)]
#     foreign_key_cols = [field.name for field in foreign_keys]

#     if additional_composite_key_col:
#         foreign_key_cols.extend(additional_composite_key_col)

#     df_new_or_updated = pd.DataFrame()
#     if len(foreign_key_cols) > 0:
#         for row in df.to_dict("records"):
#             query_obj = db_class.objects.filter(**{key: row[key] for key in foreign_key_cols})
#             if len(query_obj) == 1:
#                 obj = query_obj.values()[0]
#                 model_instance = query_obj[0]
                
#                 del obj[pk_col]
#                 for i in range(len(foreign_keys)):
#                     obj[foreign_key_cols[i]] = getattr(model_instance, foreign_key_cols[i])
#                     del obj[f'{foreign_key_cols[i]}_id']
#                 if len(datetime_col) > 0:
#                     for i in row.keys():
#                         if not pd.isna(row[i]) and getattr(model_instance, i) != row[i]:
#                             setattr(model_instance, i, row[i])
#                             model_instance.save()
#                     df_new_or_updated = df_new_or_updated.append(convert_object_to_df(model_instance))
#                 else:
#                     new_obj, created = db_class.objects.update_or_create(
#                         **obj, defaults=row
#                     )
#                     if created == True:
#                         df_new_or_updated = df_new_or_updated.append(convert_object_to_df(new_obj))
#             else:
#                 new_obj = db_class.objects.create(**row)
#                 df_new_or_updated = df_new_or_updated.append(convert_object_to_df(new_obj))
#         return df_new_or_updated
    
#     else:
#         pk_col = db_class._meta.pk.name
#         for row in df.to_dict("records"):
#             if not db_class.objects.filter(**row).exists():
#                 query_obj = db_class.objects.filter(**{pk_col:row[pk_col]})
#                 if len(query_obj) == 1:
#                     obj = query_obj.values()[0]
#                     new_obj, created = db_class.objects.update_or_create(
#                         **obj, defaults=row
#                     )
#                 else:
#                     new_obj = db_class.objects.create(**row)
#                     df_new_or_updated = df_new_or_updated.append(convert_object_to_df(new_obj, include_pk=True))
#         return df_new_or_updated
    

# def convert_object_to_df(object, include_pk=False):
#     '''
#     Takes in a Django Model object, and boolean parameter indicating whether to include the primary key
#     Return a Pandas DataFrame (of 1 row)
#     '''
#     if not include_pk:
#         col_lst = [col.name for col in object._meta.fields if not col.primary_key]
#     else:
#         col_lst = [col.name for col in object._meta.fields]

#     return pd.DataFrame({k: [getattr(object, k)] for k in col_lst})


# def fetch_all_data():

#     #----------------------- Drop All Records, starting with Associative Tables -----------------------#
#     # Derived Tables
#     TransactionSchedule.objects.all().delete()
    
#     # Associative Tables
#     Model_List.objects.all().delete()
#     InvestmentLinkTransactionWorkflow.objects.all().delete()
#     InvestmentTeamDetailsInfo.objects.all().delete()
#     InvestmentInvestmentCounterpartyLinksInfo.objects.all().delete()
#     InvestmentLinkLinkInstruments.objects.all().delete()
#     InvestmentLinkChildTransactions.objects.all().delete()
#     InvestmentCountryMixInformation.objects.all().delete()
#     InvestmentApprovedCommitmentInformation.objects.all().delete()
#     InvestmentDeals.objects.all().delete()
#     HR.objects.all().delete()

#     # Entity
#     Users.objects.all().delete()
#     InvestmentLink.objects.all().delete()
#     LegalCommitment.objects.all().delete()
#     Transaction.objects.all().delete()
#     Investment.objects.all().delete()
#     Instrument.objects.all().delete()
#     Deals.objects.all().delete()

#     #----------------------- HR Dummy -----------------------#
#     df_hr = pd.read_csv(os.path.join(os.getcwd(), "data/HR.csv"))
#     df_hr = process_hr(df_hr)
#     lst_of_hr = convert_df_to_lst_of_table_objects(df_hr, HR)
#     HR.objects.bulk_create(lst_of_hr)

#     #----------------------- Load Legal Commitments -----------------------#
#     df_legal_commitments = pd.read_csv(os.path.join(os.getcwd(), "data/LegalCommitment.csv"))
#     df_legal_commitments = process_legal_commitments(df_legal_commitments)
#     lst_of_legal_commitments = convert_df_to_lst_of_table_objects(df_legal_commitments, LegalCommitment)
#     LegalCommitment.objects.bulk_create(lst_of_legal_commitments)

#     #----------------------- Load Investment Links -----------------------#
#     df_investment_link = pd.read_csv(os.path.join(os.getcwd(), "data/InvestmentLink.csv"))
#     df_investment_link = process_investment_links(df_investment_link)
#     list_of_investment_link = convert_df_to_lst_of_table_objects(df_investment_link, InvestmentLink)
#     InvestmentLink.objects.all().delete()
#     InvestmentLink.objects.bulk_create(list_of_investment_link)

#     #----------------------- Load Transaction Workflow -----------------------#
#     df_transaction_workflow = pd.read_csv(os.path.join(os.getcwd(), "data/TransactionNotice.csv"))
#     df_transaction_workflow = process_transaction(df_transaction_workflow)
#     lst_of_transaction_workflow = convert_df_to_lst_of_table_objects(df_transaction_workflow, Transaction)
#     Transaction.objects.bulk_create(lst_of_transaction_workflow)

#     #----------------------- Load Investment -----------------------#
#     df_investment = pd.read_csv(os.path.join(os.getcwd(), "data/Investment.csv"))
#     df_investment = process_investment(df_investment)
#     lst_of_investment = convert_df_to_lst_of_table_objects(df_investment, Investment)
#     Investment.objects.bulk_create(lst_of_investment)

#     #----------------------- Load Deals -----------------------#
#     df_deals = pd.read_csv(os.path.join(os.getcwd(), "data/Deals.csv"))
#     df_deals = process_deals(df_deals)
#     list_of_deals = convert_df_to_lst_of_table_objects(df_deals, Deals)
#     Deals.objects.bulk_create(list_of_deals)

#     #----------------------- Load Instrument -----------------------#
#     df_instrument = pd.read_csv(os.path.join(os.getcwd(), "data/Instrument.csv"))
#     df_instrument = process_instrument(df_instrument)
#     list_of_instruments = convert_df_to_lst_of_table_objects(df_instrument, Instrument)
#     Instrument.objects.bulk_create(list_of_instruments)

#     #----------------------- Load Investment - Team Details Info (Associative Table) -----------------------#
#     df_InvestmentTeamDetailsInfo = pd.read_csv(os.path.join(os.getcwd(), "data/Investment-TeamDetailsInfo.csv"))
#     df_InvestmentTeamDetailsInfo = process_investment_team_details_info(df_InvestmentTeamDetailsInfo)
#     lst_of_InvestmentTeamDetailsInfo = convert_df_to_lst_of_table_objects(df_InvestmentTeamDetailsInfo, InvestmentTeamDetailsInfo)
#     InvestmentTeamDetailsInfo.objects.bulk_create(lst_of_InvestmentTeamDetailsInfo)

#     #----------------------- Load Investment - Investment Counterparty Links Info (Associative Table) -----------------------#
#     df_InvestmentCounterpartyLinksInfo = pd.read_csv(os.path.join(os.getcwd(), "data/Investment-InvestmentCounterpartyLinksInfo.csv"))
#     df_InvestmentCounterpartyLinksInfo = process_investment_counter_party_links_info(df_InvestmentCounterpartyLinksInfo)
#     lst_of_InvestmentCounterpartyLinksInfo = convert_df_to_lst_of_table_objects(df_InvestmentCounterpartyLinksInfo, InvestmentInvestmentCounterpartyLinksInfo)
#     InvestmentInvestmentCounterpartyLinksInfo.objects.bulk_create(lst_of_InvestmentCounterpartyLinksInfo)

#     #----------------------- Load Investment Link - Link Instruments (Associative Table) -----------------------#
#     df_InvestmentLinkLinkInstruments = pd.read_csv(os.path.join(os.getcwd(), "data/InvestmentLink-LinkInstruments.csv"))
#     df_InvestmentLinkLinkInstruments = process_investment_link_link_instruments(df_InvestmentLinkLinkInstruments)
#     lst_of_InvestmentLinkLinkInstruments = convert_df_to_lst_of_table_objects(df_InvestmentLinkLinkInstruments, InvestmentLinkLinkInstruments)
#     InvestmentLinkLinkInstruments.objects.bulk_create(lst_of_InvestmentLinkLinkInstruments)

#     #----------------------- Load Investment Link - Child Transactions (Associative Table) -----------------------#
#     df_InvestmentLinkChildTransactions = pd.read_csv(os.path.join(os.getcwd(), "data/InvestmentLink-ChildTransactions.csv"))
#     df_InvestmentLinkChildTransactions = process_investment_link_child_transactions(df_InvestmentLinkChildTransactions)
#     lst_of_InvestmentLinkChildTransactions = convert_df_to_lst_of_table_objects(df_InvestmentLinkChildTransactions, InvestmentLinkChildTransactions)
#     InvestmentLinkChildTransactions.objects.bulk_create(lst_of_InvestmentLinkChildTransactions)

#     #----------------------- Load Investment Link Transaction Workflow (Associative Table) -----------------------#
#     df_investment_link_transaction_workflow = pd.read_csv(os.path.join(os.getcwd(), "data/InvestmentLink-TransactionWorkFlow.csv"))
#     df_investment_link_transaction_workflow = process_investment_link_transaction_workflow(df_investment_link_transaction_workflow)
#     lst_of_inv_link_transaction = convert_df_to_lst_of_table_objects(df_investment_link_transaction_workflow, InvestmentLinkTransactionWorkflow)
#     InvestmentLinkTransactionWorkflow.objects.bulk_create(lst_of_inv_link_transaction)

#     #----------------------- Load Investment Link Legal Commitments (Associative Table) -----------------------#
#     df_investment_link_legal_commitments = pd.read_csv(os.path.join(os.getcwd(), "data/InvestmentLink-LinkLegalCommitments.csv"))    
#     df_investment_link_legal_commitments = process_investment_link_legal_commitments(df_investment_link_legal_commitments)
#     lst_of_inv_link_legal_commitments = convert_df_to_lst_of_table_objects(df_investment_link_legal_commitments, InvestmentLinkLegalCommitments)
#     InvestmentLinkLegalCommitments.objects.bulk_create(lst_of_inv_link_legal_commitments)

#     #----------------------- Load Investment - Approved Commitment Information (Associative Table) -----------------------#
#     df_InvestmentApprovedCommitmentInformation = pd.read_csv(os.path.join(os.getcwd(), "data/Investment-ApprovedCommitmentInformation.csv"))
#     df_InvestmentApprovedCommitmentInformation = process_investment_approved_commitment(df_InvestmentApprovedCommitmentInformation)
#     list_of_investment_approvedcommitment = convert_df_to_lst_of_table_objects(df_InvestmentApprovedCommitmentInformation, InvestmentApprovedCommitmentInformation)
#     InvestmentApprovedCommitmentInformation.objects.bulk_create(list_of_investment_approvedcommitment)

#     #----------------------- Load Investment - Country Mix Information (Associative Table) -----------------------#
#     df_InvestmentCountryMixInformation = pd.read_csv(os.path.join(os.getcwd(), "data/Investment-CountryMixInformation.csv"))
#     df_InvestmentCountryMixInformation = process_investment_country_mix(df_InvestmentCountryMixInformation)
#     list_of_investment_countrymix = convert_df_to_lst_of_table_objects(df_InvestmentCountryMixInformation, InvestmentCountryMixInformation)
#     InvestmentCountryMixInformation.objects.bulk_create(list_of_investment_countrymix)

#     #----------------------- Load Investment - Deals (Associative Table) -----------------------#
#     df_InvestmentDeals = pd.read_csv(os.path.join(os.getcwd(), "data/Investment-Deals.csv"))
#     df_InvestmentDeals = process_investment_deals(df_InvestmentDeals)
#     list_of_investment_deals = convert_df_to_lst_of_table_objects(df_InvestmentDeals, InvestmentDeals)
#     InvestmentDeals.objects.bulk_create(list_of_investment_deals)

#     #----------------------- Load Transaction Schedule (Derived Table) -----------------------#
#     df_past_transaction_schedule = process_transaction_schedule(pd.DataFrame())
#     list_of_schedule = convert_df_to_lst_of_table_objects(df_past_transaction_schedule, TransactionSchedule)
#     TransactionSchedule.objects.bulk_create(list_of_schedule)

#     return Response(status=status.HTTP_200_OK)