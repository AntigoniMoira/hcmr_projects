import json
import re
from datetime import datetime
from decimal import Decimal

#from django
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db.models import Q
from django.db import transaction, connection
from django.db.models.fields import Field
from django.contrib.auth import get_user_model, authenticate, login, logout, get_user
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect,csrf_exempt

#from my files
from .serializers import (
    PlatformSerializer,
    DataSerializer,
    InstitutionSerializer,
    ParameterSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    DeepObservAllDataSerializer,
    DeepObservDataSerializer,
    FerryboxSerializer,
    NoDvalqcDataSerializer,
    Cdf_InstitutionSerializer,
    OnlineDataSerializer,
)
from .models import (
    Ferrybox,
    getModel,
    Platform,
    Institution,
    Parameter,
    DeepObservgetModel,
    getModel_no_dvalqc,
    Cdf_Institution,
    OnlineData,
)
from .filters import (
    PlatformFilter,
    InstitutionFilter,
    ParameterFilter,
    FerryboxFilter,
    Cdf_InstitutionFilter,
)

from .paginations import PlatformPagination
from .lookups import NotEqual
from .custom_permissions import UserPermission

#from rest_framework
from rest_framework import generics, renderers
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from oauth2_provider.views.generic import ProtectedResourceView, ScopedProtectedResourceView
from oauth2_provider.decorators import protected_resource
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope, IsAuthenticatedOrTokenHasScope

from .utils import cURL_request
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string


class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        #return HttpResponse('Hello, OAuth2!')
        return JsonResponse({'data': 'Hello from OAuth2!'})

def index(request):
    if not request.user.is_authenticated:
        return redirect('/api/login/')
    else:
        return render(request, 'api/index.html')

@login_required
def help(request):
   # return render(request, 'api/help.html')
   return JsonResponse({'data': 'Hello from OAuth2!'})

def poseidon_db(request):
    return render(request, 'api/poseidon_db.html')

class PlatformList(generics.ListAPIView):
    #authentication_classes = [OAuth2Authentication]
    #permission_classes = [IsAuthenticatedOrTokenHasScope, UserPermission]
    #required_scopes = ['read']
    queryset = Platform.objects.all()
    #Only staff users allowed
    #permission_classes = (UserPermission, )
    serializer_class = PlatformSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = PlatformFilter
    #pagination_class = PlatformPagination
    ordering_fields = ['id']

    def post (self, request, *args, **kwargs):
        body_unicode=request.body.decode('utf-8')
        prejson = json.loads(body_unicode)
        datalist = prejson['data']
        try:
            with transaction.atomic():
                for i in range(len(datalist)):
                    inst = Institution.objects.get(id=datalist[i]['inst'])
                    obj, created = Platform.objects.update_or_create(
                                        pid = datalist[i]['pid'],
                                        tspr = datalist[i]['tspr'],
                                        type = datalist[i]['type'],
                                        defaults={
                                                'pid' : datalist[i]['pid'],
                                                'tspr' : datalist[i]['tspr'],
                                                'type' : datalist[i]['type'],
                                                'dts' : datalist[i]['dts'],
                                                'dte' : datalist[i]['dte'],
                                                'lat' : datalist[i]['lat'],
                                                'lon' : datalist[i]['lon'],
                                                'status' : datalist[i]['status'],
                                                'params' : datalist[i]['params'],
                                                'platform_code' : datalist[i]['platform_code'],
                                                'wmo' : datalist[i]['wmo'],
                                                'pi_name' : datalist[i]['pi_name'],
                                                'author' : datalist[i]['author'],
                                                'contact' : datalist[i]['contact'],
                                                'island' : datalist[i]['island'],
                                                'pl_name' : datalist[i]['pl_name'],
                                                'inst_ref' : datalist[i]['inst_ref'],
                                                'assembly_center' : datalist[i]['assembly_center'],
                                                'site_code' : datalist[i]['site_code'],
                                                'source' : datalist[i]['source'],
                                                'cdf_inst' : datalist[i]['cdf_inst'],
                                                'inst' : inst},
                                    )
        except Exception:
            return JsonResponse({
                'success': False
                })
        return JsonResponse({
                'success': True
                })

class InstitutionList(generics.ListAPIView):
    queryset = Institution.objects.all()
    #Only staff users allowed
    #permission_classes = (UserPermission, )
    serializer_class = InstitutionSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = InstitutionFilter
    ordering_fields = ['id']

class Cdf_InstitutionList(generics.ListAPIView):
    queryset = Cdf_Institution.objects.all()
    serializer_class = Cdf_InstitutionSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = Cdf_InstitutionFilter
    ordering_fields = ['id']

    def post (self, request, *args, **kwargs):
        name=request.POST.get('name', None)
        inst=Cdf_Institution.objects.filter(name=name)
        if inst.exists():
            return JsonResponse({ "success" : False})
        else:
            institution=Institution.objects.get(id=66)
            new_cdf_inst=Cdf_Institution.objects.create(name=name, inst_id=institution)
            new_cdf_inst.save()
            return JsonResponse({ "success" : True, "id" : new_cdf_inst.id})



class ParameterList(generics.ListAPIView):
    queryset = Parameter.objects.all()
    #Only staff users allowed
    #permission_classes = (UserPermission, )
    serializer_class = ParameterSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = ParameterFilter
    ordering_fields = ['id']

    #Create or update fields in data."<platform>" tables and create parameter in metadata."parameters" if not exists
    def post (self, request, *args, **kwargs):
        #print(request.data)
        body_unicode=request.body.decode('utf-8')
        prejson = json.loads(body_unicode)
        metalist = prejson['meta']
        try:
            with transaction.atomic():
                for i in range(len(metalist)):
                    obj, created = Parameter.objects.get_or_create(
                                        pname = metalist[i]['pname'],
                                        defaults={
                                                'pname' : metalist[i]['pname'],
                                                'unit' : metalist[i]['init'],
                                                'stand_name' : metalist[i]['stand_name'],
                                                'long_name' : metalist[i]['long_name'],
                                                'fval' : metalist[i]['fval'],
                                                'fval_qc' : metalist[i]['fval_qc'],},
                                    )
        except Exception:
            return JsonResponse({
                'success': False
                })
        return JsonResponse({
                'success': True
                })

#GET: returns a json with data
#POST: takes a json and update DB
class DataList(generics.ListAPIView):
    #Only staff users allowed
    #permission_classes = (UserPermission, )

    def get_queryset(self):
        platform = self.kwargs['platform']
        t = getModel()
        t._meta.db_table='data\".\"'+platform
        queryset=t.objects.all()
        return queryset
    
    def get_serializer_class(self):
        platform = self.kwargs['platform']
        t = getModel()
        t._meta.db_table='data\".\"'+platform
        serializer_class = DataSerializer
        serializer_class.Meta.model=t
        return serializer_class

    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    Field.register_lookup(NotEqual)
    filter_fields = {
            #available filters:'exact','ne', 'lt', 'gt', 'lte', 'gte', 'in', icontains
            'id': ['exact', 'ne', 'in', 'lte'], #notin
            'dt': ['lt', 'gt', 'lte', 'gte', 'icontains'],
            'lat': ['lt', 'gt', 'lte', 'gte'],
            'lon': ['lt', 'gt', 'lte', 'gte'],
            'posqc': ['exact', 'ne', 'in','lt', 'gt', 'lte', 'gte'], #notin
            'pres': ['lt', 'gt', 'lte', 'gte'],
            'presqc': ['exact', 'ne', 'in', 'lt', 'gt', 'lte', 'gte'], #notin
            'param': ['exact'],
            'param__id' : ['exact','ne', 'in'], #notin
            'val': ['lt', 'gt', 'lte', 'gte'],
            'valqc': ['exact', 'ne', 'in', 'lt', 'gt', 'lte', 'gte'] #notin
        }
    ordering_fields = ['id']


    #Create or update fields in data."<platform>" tables and create parameter in metadata."parameters" if not exists
    def post (self, request, *args, **kwargs):
        platform = self.kwargs['platform']
        t = getModel()
        t._meta.db_table='data\".\"'+platform
        body_unicode=request.body.decode('utf-8')
        prejson = json.loads(body_unicode)
        datalist = prejson['data']
        try:
            with transaction.atomic():
                for i in range(len(datalist)):
                    par=Parameter.objects.get(pname=datalist[i]['param'])
                    obj, created = t.objects.update_or_create(
                                        dt = datalist[i]['dt'],
                                        lat = datalist[i]['lat'],
                                        lon = datalist[i]['lon'],
                                        param = par,
                                        pres = datalist[i]['pres'],
                                        defaults={
                                                'dt' : datalist[i]['dt'],
                                                'lat' : datalist[i]['lat'],
                                                'lon' : datalist[i]['lon'],
                                                'posqc' : datalist[i]['posqc'],
                                                'pres' : datalist[i]['pres'],
                                                'presqc' : datalist[i]['presqc'],
                                                'param' : par,
                                                'val' : datalist[i]['val'],
                                                'valqc' : datalist[i]['valqc'],
                                                'dvalqc' : datalist[i]['dvalqc']},
                                    )
        except Exception:
            return JsonResponse({
                'success': False
                })
        return JsonResponse({
                'success': True
                })

class DeepObservAllDataList(generics.ListAPIView):

    def get_queryset(self):
        platform = self.kwargs['platform']
        t = DeepObservgetModel()
        t._meta.db_table='data\".\"'+platform
        queryset=t.objects.all()
        return queryset
    
    def get_serializer_class(self):
        platform = self.kwargs['platform']
        t = DeepObservgetModel()
        t._meta.db_table='data\".\"'+platform
        serializer_class = DeepObservAllDataSerializer
        serializer_class.Meta.model=t
        return serializer_class

    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    Field.register_lookup(NotEqual)
    filter_fields = {
            #available filters:'exact','ne', 'lt', 'gt', 'lte', 'gte', 'in', icontains
            'id': ['exact', 'ne', 'in'], #notin
            'dt': ['lt', 'gt', 'lte', 'gte', 'icontains'],
            'lat': ['lt', 'gt', 'lte', 'gte'],
            'lon': ['lt', 'gt', 'lte', 'gte'],
            'posqc': ['exact', 'ne', 'in','lt', 'gt', 'lte', 'gte'], #notin
            'pres': ['lt', 'gt', 'lte', 'gte'],
            'presqc': ['exact', 'ne', 'in', 'lt', 'gt', 'lte', 'gte'], #notin
            'param': ['exact'],
            'param__id' : ['exact','ne', 'in'], #notin
            'val': ['lt', 'gt', 'lte', 'gte'],
            'valqc': ['exact', 'ne', 'in', 'lt', 'gt', 'lte', 'gte'], #notin
            'rval': ['lt', 'gt', 'lte', 'gte'],
            'rvalqc': ['exact', 'ne', 'in', 'lt', 'gt', 'lte', 'gte'] #notin
        }
    ordering_fields = ['id']


    #Create or update fields in data."<platform>" tables and create parameter in metadata."parameters" if not exists
    def post (self, request, *args, **kwargs):
        platform = self.kwargs['platform']
        t = DeepObservgetModel()
        t._meta.db_table='data\".\"'+platform
        prejson = json.loads(request.body)
        try:
            datalist = prejson['data']
            with transaction.atomic():
                for i in range(len(datalist)):
                    par=Parameter.objects.get(pname=datalist[i]['param'])
                    obj, created = t.objects.update_or_create(
                                        dt = datalist[i]['dt'],
                                        lat = datalist[i]['lat'],
                                        lon = datalist[i]['lon'],
                                        param = par,
                                        pres = datalist[i]['pres'],
                                        defaults={
                                                'dt' : datalist[i]['dt'],
                                                'lat' : datalist[i]['lat'],
                                                'lon' : datalist[i]['lon'],
                                                'posqc' : datalist[i]['posqc'],
                                                'pres' : datalist[i]['pres'],
                                                'presqc' : datalist[i]['presqc'],
                                                'param' : par,
                                                'val' : datalist[i]['val'],
                                                'valqc' : datalist[i]['valqc'],
                                                'dvalqc' : datalist[i]['dvalqc'],
                                                'rval' : datalist[i]['rval'],
                                                'rvalqc' : datalist[i]['rvalqc']},
                                    )
        except Exception:
            return JsonResponse({
                'success': False
                })
        return JsonResponse({
                'success': True
                })

class DeepObservDataList(generics.ListAPIView):

    def get_queryset(self):
        platform = self.kwargs['platform']
        t = DeepObservgetModel()
        t._meta.db_table='data\".\"'+platform
        queryset=t.objects.all()
        return queryset
    
    def get_serializer_class(self):
        platform = self.kwargs['platform']
        t = DeepObservgetModel()
        t._meta.db_table='data\".\"'+platform
        serializer_class = DeepObservDataSerializer
        serializer_class.Meta.model=t
        return serializer_class

    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    Field.register_lookup(NotEqual)
    filter_fields = {
            #available filters:'exact','ne', 'lt', 'gt', 'lte', 'gte', 'in', icontains
            'id': ['exact', 'ne', 'in'], #notin
            'dt': ['lt', 'gt', 'lte', 'gte', 'icontains'],
            'lat': ['lt', 'gt', 'lte', 'gte'],
            'lon': ['lt', 'gt', 'lte', 'gte'],
            'posqc': ['exact', 'ne', 'in','lt', 'gt', 'lte', 'gte'], #notin
            'pres': ['lt', 'gt', 'lte', 'gte'],
            'presqc': ['exact', 'ne', 'in', 'lt', 'gt', 'lte', 'gte'], #notin
            'param': ['exact'],
            'param__id' : ['exact','ne', 'in'], #notin
            'val': ['lt', 'gt', 'lte', 'gte'],
            'valqc': ['exact', 'ne', 'in', 'lt', 'gt', 'lte', 'gte'] #notin
        }
    ordering_fields = ['id']


class FerryboxDataList(generics.ListAPIView):
    queryset = Ferrybox.objects.all()
    serializer_class = FerryboxSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = FerryboxFilter
    ordering_fields = ['id']

###############################################################################################
#Views for db_download service

#returns platforms
#@login_required()
def poseidon_platforms_with_measurements_between(request):
    start_date=request.GET.get('start_date', '')
    end_date=request.GET.get('end_date', '')

    # Get a cursor on the connection
    cursor = connection.cursor()

    # Now, callproc to the name of the procedure/function and pass a list of parameters inside
    cursor.callproc("data.poseidon_platforms_with_measurements_between", [start_date, end_date])

    # Fetch new a list of all the results
    results = cursor.fetchall()
    # Close the cursor
    cursor.close()

    data = []
    for i in range(len(results)):
        d ={}
        d['platform'] = results[i][0]
        data.append(d)

    return JsonResponse({ "data" : data})

#returns platform's parameters
#@login_required()
def poseidon_platform_parameters_with_measurements_between(request):
    platform_name=request.GET.get('platform', '')
    start_date=request.GET.get('start_date', '')
    end_date=request.GET.get('end_date', '')

    # Get a cursor on the connection
    cursor = connection.cursor()

    # Now, callproc to the name of the procedure/function and pass a list of parameters inside
    cursor.callproc("public.poseidon_platform_parameters_with_measurements_between", [platform_name, start_date, end_date])

    # Fetch new a list of all the results
    results = cursor.fetchall()
    # Close the cursor
    cursor.close()
    
    return JsonResponse({ "data" : results[0][0]})

class Poseidon_db_List(generics.ListAPIView):
    #Only staff users allowed
    #permission_classes = (UserPermission, )

    def get_queryset(self):
        platform = self.kwargs['platform']
        t = getModel_no_dvalqc()
        t._meta.db_table='public\".\"'+platform
        queryset=t.objects.all()
        return queryset
    
    def get_serializer_class(self):
        platform = self.kwargs['platform']
        t = getModel_no_dvalqc()
        t._meta.db_table='public\".\"'+platform
        serializer_class = NoDvalqcDataSerializer
        serializer_class.Meta.model=t
        return serializer_class

    filter_backends = (DjangoFilterBackend,)
    Field.register_lookup(NotEqual)
    filter_fields = {
            'dt': ['lt', 'gt', 'lte', 'gte', 'icontains'],
            'pres': ['lt', 'gt', 'lte', 'gte', 'in'],
            'param__id' : ['exact','ne', 'in'], 
        }

def poseidon_db_unique_dt(request):
    platform_name=request.GET.get('platform', '')
    start_date=request.GET.get('start_date', '')
    end_date=request.GET.get('end_date', '')
    params=request.GET.get('params', '').split(',')
    print(params)
    t = getModel_no_dvalqc()
    t._meta.db_table='public\".\"'+platform_name
    queryset_dt=t.objects.values('dt').filter(Q(param__in=params), Q(dt__gte=start_date), Q(dt__lte=end_date)).distinct('dt')
    queryset_pres=t.objects.values('pres').filter(Q(param__in=params), Q(dt__gte=start_date), Q(dt__lte=end_date)).order_by('pres').distinct('pres')
    dt_list = [ obj for obj in queryset_dt ]
    count_dt=len(dt_list)
    pres_list = [ obj for obj in queryset_pres ]
    count_pres=len(pres_list)
    return JsonResponse({'count_dt': count_dt,'date' : dt_list, 'count_pres': count_pres,'pressure' : pres_list})

# End of Views for db_download service
################################################################################################################
#Views for user authentication
def TermsAndConditions (request):
    return render(request, 'api/terms.html')

User = get_user_model()

class UserCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    #renderer_classes = [renderers.JSONRenderer]
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        return render(request, 'api/signup.html')

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=False):
            new_data = serializer.data
            serializer.create(serializer.data)
            subject='[HCMR] Activate User'
            name=new_data['firstname'] + ' ' +new_data['lastname']
            html_content=render_to_string('api/activate_user_mail.html', {'name': name, 'country': new_data['country'],
            'institution': new_data['institution'], 'email': new_data['email'], 'description': new_data['description']})
            send_mail(subject, name, 'antmoira@gmail.com', ['antmoira@gmail.com'], fail_silently=False, html_message=html_content,)
            response = JsonResponse({
                'success': True
            })
            return response
        else:
            print(serializer.errors)
            return JsonResponse({
                'success': False,
                'message': serializer.errors['non_field_errors'][0]
            })

class ActivateUser(APIView):
    #permission_classes = [IsAuthenticatedOrTokenHasScope, UserPermission]
    def get(self, request, *args, **kwargs):
        users=User.objects.filter(is_active=False)
        return render(request, 'api/activate_users.html', {'users': users})

    def post(self, request, *args, **kwargs):
        email=request.data['email']
        try:
            user=User.objects.get(email=email)
            user.is_active=True
            user.save()
            subject='[HCMR] Account Activation'
            name=user.first_name
            html_content=render_to_string('api/accept_user_mail.html', {'name': name})
            send_mail(subject, name, 'antmoira@gmail.com', [email], fail_silently=False, html_message=html_content,)
            return JsonResponse({
                'success': True
            })
        except Exception:
            return JsonResponse({
                'success': False,
                'message': 'An error occurred. Please try again later.'
            })

class DeleteUser(APIView):
    #permission_classes = [IsAuthenticatedOrTokenHasScope, UserPermission]

    def post(self, request, *args, **kwargs):
        email=request.data['email']
        reason=request.data['reason']
        try:
            user=User.objects.get(email=email)
            user.delete()
            subject='[HCMR] Your request has been rejected.'
            name=user.first_name
            html_content=render_to_string('api/reject_user_mail.html', {'name': name, 'reason':reason})
            send_mail(subject, name, 'antmoira@gmail.com', [email], fail_silently=False, html_message=html_content,)
            return JsonResponse({
                'success': True
            })
        except Exception:
            return JsonResponse({
                'success': False,
                'message': 'An error occurred. Please tre again later.'
            })


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=False):
            new_data = serializer.data
            user = authenticate(request, username=new_data['username'], password=new_data['password'])
            login(request, user)
            new_data['password']=''
            response = JsonResponse({
                'success': True
            })
            return response
        else:
            print(serializer.errors)
            return JsonResponse({
                'success': False,
                'message': serializer.errors['non_field_errors'][0]
            })

    def get(self, request, *args, **kwargs):
        print(request.user)
        if request.user.is_authenticated:
            return HttpResponseRedirect('../index')
        return render(request, 'api/login.html')

@login_required()
def logout_user(request):
    #request.user.auth_token.delete()
    response = HttpResponseRedirect('/api/login/')
    logout(request)
    return response

#End of Views for user authentication
################################################################################################################

#Start of Views for online_data service
################################################################################################################

class OnlineDataList(generics.ListAPIView):
    queryset = OnlineData.objects.all()
    #Only staff users allowed
    #permission_classes = (UserPermission, )
    serializer_class = OnlineDataSerializer
    #filter_backends = (DjangoFilterBackend, OrderingFilter,)
    #filter_class = InstitutionFilter
    ordering_fields = ['platform']


def ts_latest_data(request, platform):
    t = getModel()
    t._meta.db_table='data\".\"'+platform
    last=t.objects.latest('dt')
    last_dt=last.dt
    latest_data=t.objects.filter(dt=last_dt)

    if (last_dt.month <10):
        start_date=str(last_dt.year)+"-0"+str(last_dt.month)
    else:
        start_date=str(last_dt.year)+"-"+str(last_dt.month)
    end_date=start_date
    
    # Get a cursor on the connection
    cursor = connection.cursor()

    # Now, callproc to the name of the procedure/function and pass a list of parameters inside
    cursor.callproc("public.poseidon_platform_parameters_with_measurements_between", [platform, start_date, end_date])

    # Fetch new a list of all the results
    results = cursor.fetchall()[0][0]
    param_string=results[0]['param']
    param_list= param_string.split("#")
    result_dict={'info':{
        'platform': platform,
        'date':last_dt,
        'lat':last.lat,
        'lon':last.lon },
        'params':{}
    }
    for i in range(0,len(param_list)):
        row=param_list[i]
        parts=re.split('\[|\]|@|\^|<|>', row)
        description=parts[0]+"["+parts[1]+"] "+parts[3] +" ("+parts[7]+")"
        if parts[1] not in result_dict['params'].keys():
            result_dict['params'][parts[1]]={}
        result_dict['params'][parts[1]][parts[3]]={
            "description": description,
            "val": 9999,
            "valqc":9
        }
    
    for i in range(0,len(latest_data)):
        parameter=latest_data[i].param.pname
        pressure=str(int(latest_data[i].pres))+"m"
        result_dict['params'][parameter][pressure]['val']=latest_data[i].val
        result_dict['params'][parameter][pressure]['valqc']=latest_data[i].valqc

    # Close the cursor
    cursor.close()
    return JsonResponse(result_dict)

def pr_latest_data(request, platform):
    t = getModel()
    t._meta.db_table='data\".\"'+platform
    last=t.objects.latest('dt')
    last_dt=last.dt
    latest_data=t.objects.filter(dt=last_dt)

    result_dict={'info':{
        'platform': platform,
        'date':last_dt,
        'lat':last.lat,
        'lon':last.lon },
        'params':{}
    }


    for i in range(0,len(latest_data)):
        parameter=latest_data[i].param.pname
        if parameter not in result_dict['params'].keys():
            result_dict['params'][parameter]=[]
        result_dict['params'][parameter].append({
            'pres': latest_data[i].pres,
            'val': latest_data[i].val,
            'valqc': latest_data[i].valqc
        })
        
    
    return JsonResponse(result_dict)

#End of Views for online_data service
################################################################################################################