from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
#from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.response import Response
from .serializers import PlatformSerializer, DataSerializer, InstitutionSerializer, ParameterSerializer
from .models import Test, getModel, Platform, Institution, Parameter
from .filters import PlatformFilter, InstitutionFilter, ParameterFilter
from .paginations import PlatformPagination
from .lookups import NotEqual
from django.db.models.fields import Field

def index(request):
    return HttpResponse('Hey')

def help(request):
    return render(request, 'api/help.html')

class PlatformList(generics.ListAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = PlatformFilter
    #pagination_class = PlatformPagination
    ordering_fields = ['id']

class InstitutionList(generics.ListAPIView):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = InstitutionFilter
    #pagination_class = PlatformPagination
    ordering_fields = ['id']

class ParameterList(generics.ListAPIView):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = ParameterFilter
    #pagination_class = PlatformPagination
    ordering_fields = ['id']

'''def platforms_data(request, platform):
    t=getModel()
    t._meta.db_table='data\".\"'+platform
    data=t.objects.all().count()
    return JsonResponse({
             'data': data
            })'''


# tis a general model for all data tables
#t = getModel()

class DataList(generics.ListAPIView):


    def get_queryset(self):
        platform = self.kwargs['platform']
        t = getModel()
        t._meta.db_table='data\".\"'+platform 
        queryset=t.objects.all()
        return queryset
    
    def get_serializer_class(self):
        platform = self.kwargs['platform']
        t= getModel()
        t._meta.db_table='data\".\"'+platform 
        serializer_class = DataSerializer
        serializer_class.Meta.model=t
        return serializer_class

    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    Field.register_lookup(NotEqual)
    filter_fields = {
            #available filters:'exact','ne', 'lt', 'gt', 'lte', 'gte', 'in', icontains
            'id': ['exact', 'ne', 'in'], #notin
            'pid': [],
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
    #pagination_class = PlatformPagination
    ordering_fields = ['id']
