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
import json
from datetime import datetime
from decimal import Decimal

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
    ordering_fields = ['id']

class ParameterList(generics.ListAPIView):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = ParameterFilter
    ordering_fields = ['id']

#GET: returns a json with data
#POST: takes a json and update DB
class DataList(generics.ListAPIView):

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


    #Create or update fields in data."<platform>" tables
    def post (self, request, *args, **kwargs):
        platform = self.kwargs['platform']
        t = getModel()
        t._meta.db_table='data\".\"'+platform
        prejson = json.loads(request.body)
        datalist = prejson['data']
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
         
