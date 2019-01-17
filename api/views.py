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
from django.views.decorators.csrf import csrf_protect, csrf_exempt

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
from rest_framework import generics, renderers, viewsets
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.decorators import permission_classes

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from oauth2_provider.views.generic import ProtectedResourceView, ScopedProtectedResourceView
from oauth2_provider.decorators import protected_resource
from oauth2_provider.contrib.rest_framework import TokenMatchesOASRequirements, TokenHasReadWriteScope, TokenHasScope

from .utils import cURL_request
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.inspectors import FilterInspector, SwaggerAutoSchema
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view

#class ApiEndpoint(ProtectedResourceView):
class ApiEndpoint(APIView):
    swagger_schema = None
    #permission_classes = [UserPermission]
    #@permission_classes((UserPermission,))
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    #permission_classes =[AllowAny]
    required_scopes = ['user']
    def get(self, request, *args, **kwargs):
        #print(request.user.is_staff)
        #return HttpResponse('Hello, OAuth2!')
        return JsonResponse({'data': 'Hello, OAuth2!'})

class NoFilterAutoSchema(SwaggerAutoSchema):
    filter_inspectors = []

dts__gte = openapi.Parameter('dt__gte', openapi.IN_QUERY, description="Start datetime. Format:  'yyyy-mm-dd hh:mm:ss' e.g. 2016-04-08 13:30:00", type=openapi.TYPE_STRING)
dte__lte = openapi.Parameter('dt__lte', openapi.IN_QUERY, description="End datetime. Format:  'yyyy-mm-dd hh:mm:ss' e.g. 2016-04-09 13:30:00", type=openapi.TYPE_STRING)
params__icontains = openapi.Parameter('params__icontains', openapi.IN_QUERY, description="Parameter's name to filter platforms. e.g. PSAL", type=openapi.TYPE_STRING)
type = openapi.Parameter('type', openapi.IN_QUERY, description="Platform's type. e.g. PF", type=openapi.TYPE_STRING)
status = openapi.Parameter('status', openapi.IN_QUERY, description="Platform's status. e.g. true", type=openapi.TYPE_BOOLEAN)
@method_decorator(name='get', decorator=swagger_auto_schema(manual_parameters= [dts__gte, dte__lte, params__icontains, type, status] ))
class PlatformList(generics.ListCreateAPIView):
    """
    View to list all Platforms in the system.

    * Requires token authentication.

    """
    
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenMatchesOASRequirements]
    required_alternate_scopes = {
        "GET": [["user"]],
        "POST": [["user", "staff", "admin"]],
    }
    swagger_schema = NoFilterAutoSchema
    #permission_classes = [AllowAny]
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = PlatformFilter
    ordering_fields = ['id']

    @swagger_auto_schema(method='post', auto_schema=None)
    @api_view(['POST'])
    def post (self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
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
            return Response({
                'success': False
                })
        return Response({
                'success': True
                })

class InstitutionList(generics.ListAPIView):
    """
    View to list all Institutions in the system.

    * Requires token authentication.

    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['user']
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = InstitutionFilter
    ordering_fields = ['id']

class Cdf_InstitutionList(generics.ListCreateAPIView):
    swagger_schema = None
    """
    View to list all Cdf_Institurions in the system.

    * Requires token authentication.
    * Only admin users are able to access.

    get:
    Return a list of all the existing cdf_Institutions.

    post:
    Create a new cdf_Institution instance.
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['admin']
    queryset = Cdf_Institution.objects.all()
    serializer_class = Cdf_InstitutionSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = Cdf_InstitutionFilter
    ordering_fields = ['id']

    @swagger_auto_schema(method='post', auto_schema=None)
    @api_view(['POST'])
    def post (self, request, *args, **kwargs):
        name = request.POST.get('name', None)
        inst = Cdf_Institution.objects.filter(name=name)
        if inst.exists():
            return Response({ "success" : False})
        else:
            institution = Institution.objects.get(id=66)
            new_cdf_inst = Cdf_Institution.objects.create(name=name, inst_id=institution)
            new_cdf_inst.save()
            return Response({ "success" : True, "id" : new_cdf_inst.id})

class ParameterList(generics.ListAPIView):
    """
    View to list all Parameters in the system.

    * Requires token authentication.

    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenMatchesOASRequirements]
    required_alternate_scopes = {
        "GET": [["user"]],
        "POST": [["user", "staff", "admin"]],
    }
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = ParameterFilter
    ordering_fields = ['id']

    @swagger_auto_schema(method='post', auto_schema=None)
    @api_view(['POST'])
    def post (self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
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
            return Response({
                'success': False
                })
        return Response({
                'success': True
                })

dt__gte = openapi.Parameter('dt__gte', openapi.IN_QUERY, description="Minimun datetime of measurement. Format:  'yyyy-mm-dd hh:mm:ss' e.g. 2016-04-08 13:30:00", type=openapi.TYPE_STRING)
dt__lte = openapi.Parameter('dt__lte', openapi.IN_QUERY, description="Maximum datetime of measurement. Format:  'yyyy-mm-dd hh:mm:ss' e.g. 2016-04-09 13:30:00", type=openapi.TYPE_STRING)
param__id__in = openapi.Parameter('param__id__in', openapi.IN_QUERY, description="List of parameters' ids to filter measurements. e.g. 26, 124", type=openapi.TYPE_STRING)
param__pname__in = openapi.Parameter('param__pname__in', openapi.IN_QUERY, description="List of parameters' names to filter measurements. e.g. PSAL, VTM02", type=openapi.TYPE_STRING)
pres__gte = openapi.Parameter('pres__gte', openapi.IN_QUERY, description="Minimum depth of measurement (Pressure). e.g. -3.0", type=openapi.TYPE_NUMBER)
pres__lte = openapi.Parameter('pres__lte', openapi.IN_QUERY, description="Maximum depth of measurement (Pressure). e.g. 100.0", type=openapi.TYPE_NUMBER)
@method_decorator(name='list', decorator=swagger_auto_schema( manual_parameters= [dt__gte, dt__lte, param__id__in, param__pname__in, pres__gte, pres__lte] ))
class DataList(viewsets.ModelViewSet):
    """
    View to list all platform's data in the system.

    * Requires token authentication.

    get:
    Return a list of all the platform's data.

    post:
    Create new platform's data instance.
    * Only admin users are able to access.
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenMatchesOASRequirements]
    required_alternate_scopes = {
        "GET": [["user"]],
        "POST": [["user", "staff", "admin"]],
    }
    
    def get_queryset(self):
        platform = self.kwargs['platform']
        t = getModel()
        t._meta.db_table = 'data\".\"'+platform
        queryset = t.objects.all()
        return queryset
    
    serializer_class = DataSerializer
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
            #'param': ['exact', 'in'],
            'param__pname': ['exact', 'in'],
            'param__id' : ['exact','ne', 'in'], #notin
            'val': ['lt', 'gt', 'lte', 'gte'],
            'valqc': ['exact', 'ne', 'in', 'lt', 'gt', 'lte', 'gte'] #notin
    }
    ordering_fields = ['id', 'pres']

    @swagger_auto_schema(method='post', auto_schema=None)
    @api_view(['POST'])
    def post(self, request, *args, **kwargs):
        #Create or update fields in data."<platform>" tables and create parameter in metadata."parameters" if not exists
        platform = self.kwargs['platform']
        t = getModel()
        t._meta.db_table = 'data\".\"'+platform
        body_unicode = request.body.decode('utf-8')
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
            return Response({
                'success': False
                })
        return Response({
                'success': True
                })

class DeepObservAllDataList(generics.ListCreateAPIView):
    swagger_schema = None
    """
    View to list Deep Observer's data (with rval & rvalqc).

    * Requires token authentication.

    get:
    Return a list of all the deep observer's data.

    post:
    Create new deep observer's data instance.
    * Only admin users are able to access.
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenMatchesOASRequirements]
    required_alternate_scopes = {
        "GET": [["user"]],
        "POST": [["user", "staff", "admin"]],
    }
    def get_queryset(self):
        platform = self.kwargs['platform']
        t = DeepObservgetModel()
        t._meta.db_table = 'data\".\"'+platform
        queryset = t.objects.all()
        return queryset
    
    '''def get_serializer_class(self):
        platform = self.kwargs['platform']
        t = DeepObservgetModel()
        t._meta.db_table = 'data\".\"'+platform
        serializer_class = DeepObservAllDataSerializer
        serializer_class.Meta.model = t
        return serializer_class'''
    serializer_class = DataSerializer

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
            return Response({
                'success': False
                })
        return Response({
                'success': True
                })

class DeepObservDataList(generics.ListAPIView):
    """
    View to list Deep Observer's data.

    * Requires token authentication.

    get:
    Return a list of all the deep observer's data.
    """
    swagger_schema = None
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['user']

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
    #serializer_class = DataSerializer

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
    """
    View to list all Ferrybox data in the system.

    * Requires token authentication.

    get:
    Return a list of all the ferrybox data.
    """
    swagger_schema = None
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['user']
    queryset = Ferrybox.objects.all()
    serializer_class = FerryboxSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = FerryboxFilter
    ordering_fields = ['id']

###############################################################################################
#Views for db_download service

#returns platforms
@protected_resource(scopes=['user'])
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
@protected_resource(scopes=['user'])
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
    swagger_schema = None
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


#Start of Views for online_data service
################################################################################################################

class OnlineDataList(generics.ListAPIView):
    swagger_schema = None
    queryset = OnlineData.objects.all()
    permission_classes = []
    serializer_class = OnlineDataSerializer
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