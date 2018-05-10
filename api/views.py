import json

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
)
from .models import (
    Ferrybox,
    getModel,
    Platform,
    Institution,
    Parameter,
    DeepObservgetModel,
    getModel_no_dvalqc,
)
from .filters import (
    PlatformFilter,
    InstitutionFilter,
    ParameterFilter,
    FerryboxFilter,
)

from .paginations import PlatformPagination
from .lookups import NotEqual
from .custom_permissions import UserPermission

#from rest_framework
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from rest_framework.permissions import (
    AllowAny,
)

from oauth2_provider.views.generic import ProtectedResourceView

from .utils import cURL_request
#from django.contrib.auth.decorators import login_required


class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')

def index(request):
    if not request.user.is_authenticated:
        return redirect('/api/login/')
    else:
        return render(request, 'api/index.html')

def help(request):
    return render(request, 'api/help.html')

def poseidon_db(request):
    return render(request, 'api/poseidon_db.html')

class PlatformList(generics.ListAPIView):
    queryset = Platform.objects.all()
    #Only staff users allowed
    permission_classes = (UserPermission, )
    serializer_class = PlatformSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = PlatformFilter
    #pagination_class = PlatformPagination
    ordering_fields = ['id']

class InstitutionList(generics.ListAPIView):
    queryset = Institution.objects.all()
    #Only staff users allowed
    permission_classes = (UserPermission, )
    serializer_class = InstitutionSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = InstitutionFilter
    ordering_fields = ['id']

class ParameterList(generics.ListAPIView):
    queryset = Parameter.objects.all()
    #Only staff users allowed
    #permission_classes = (UserPermission, )
    serializer_class = ParameterSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = ParameterFilter
    ordering_fields = ['id']

#GET: returns a json with data
#POST: takes a json and update DB
class DataList(generics.ListAPIView):
    #Only staff users allowed
    permission_classes = (UserPermission, )

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


    #Create or update fields in data."<platform>" tables and create parameter in metadata."parameters" if not exists
    def post (self, request, *args, **kwargs):
        platform = self.kwargs['platform']
        t = getModel()
        t._meta.db_table='data\".\"'+platform
        prejson = json.loads(request.body)
        metalist = prejson['meta']
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
                                            'dvalqc' : datalist[i]['dvalqc']},
                                )
        return Response(created)

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
        metalist = prejson['meta']
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
        return Response(created)
         


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

################################################################################################################
#views for user authentication

User = get_user_model()

class UserCreateAPIView(generics.CreateAPIView):
    #permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

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
            #token = Token.objects.create(user=user)
            curl_res = cURL_request(new_data['username'], new_data['password'])
            access_token=json.loads(curl_res.text)['access_token']
            new_data['password']=''
            response = JsonResponse({
                'success': True,
                'redirectUri': reverse('index')
            })
            response.set_cookie('access_token', access_token)
            return response
        else:
            return JsonResponse({
                'success': False,
                'message': serializer.errors['non_field_errors'][0]
            })

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('../index')
        return render(request, 'api/login.html')

def logout_user(request):
    #request.user.auth_token.delete()
    response = HttpResponseRedirect('/api/login/')
    response.delete_cookie('access_token')
    logout(request)
    return response


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
            #'presqc': ['exact', 'ne', 'in', 'lt', 'gt', 'lte', 'gte'], #notin
            #'param': ['exact'],
            'param__id' : ['exact','ne', 'in'], #notin
            #'val': ['lt', 'gt', 'lte', 'gte'],
            #'valqc': ['exact', 'ne', 'in', 'lt', 'gt', 'lte', 'gte'] #notin
        }
