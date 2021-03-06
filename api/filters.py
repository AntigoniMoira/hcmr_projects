from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django_filters import rest_framework as filters
from distutils.util import strtobool
from .models import Platform, Institution, Parameter, Ferrybox, Cdf_Institution, getModel
from django import forms
#imports for custom lookups
from .lookups import NotEqual, NotIn
from django.db.models.fields import Field

BOOLEAN_CHOICES = (('false', 'False'), ('true', 'True'),)

class PlatformFilter(FilterSet):
    Field.register_lookup(NotEqual)
    #Field.register_lookup(NotIn)
    status = filters.TypedChoiceFilter(choices=BOOLEAN_CHOICES, coerce=strtobool)

    class Meta:
        model = Platform
        fields = {
            #filters:'exact','ne', 'lt', 'gt', 'lte', 'gte', 'in', icontains
            'id': ['exact', 'ne', 'in'], #notin
            'pid': ['exact', 'ne','in'], #notin
            'tspr': ['exact', 'ne'],
            'type': ['exact', 'ne', 'in'], #notin
            'inst': ['exact'], #einai kai kleidi gia institutions opote ftiaxnei drop down me ta institutions
            'inst__id': ['exact', 'in'],
            'dts': [ 'lt', 'gt', 'lte', 'gte', 'icontains'],
            'dte': [ 'lt', 'gt', 'lte', 'gte', 'icontains'],
            'lat':  ['lt', 'gt', 'lte', 'gte'],
            'lon':  ['lt', 'gt', 'lte', 'gte'],
            'status': [],
            'params' : ['icontains'], 
            'platform_code': [],
            'wmo': ['exact', 'ne', 'icontains'],
            'pi_name' : ['icontains'], 
            'author' : [],
            'contact' : [],
            'island': [],
            'pl_name' : [],
            'inst_ref' : [],
            'assembly_center' : ['exact', 'ne', 'in'],
            'site_code' : [],
            'source' : [],
            'cdf_inst': ['exact']

        }

class InstitutionFilter(FilterSet):
    Field.register_lookup(NotEqual)
    #Field.register_lookup(NotIn)

    class Meta:
        model = Institution
        fields = {
            #filters:'exact','ne', 'lt', 'gt', 'lte', 'gte', 'in', icontains
            'id': ['exact', 'ne', 'in'], #notin
            'name_native' : ['exact', 'ne', 'icontains'],
            'abrv' : ['exact', 'ne', 'in', 'icontains'], #notin
            'country' : ['exact', 'ne', 'in', 'icontains'], #notin
            'cdf_name' : [] 
        }

class Cdf_InstitutionFilter(FilterSet):
    Field.register_lookup(NotEqual)
    #Field.register_lookup(NotIn)

    class Meta:
        model = Cdf_Institution
        fields = {
            #filters:'exact','ne', 'lt', 'gt', 'lte', 'gte', 'in', icontains
            'id': ['exact', 'ne', 'in'], #notin
            'name' : ['exact', 'ne', 'icontains'],
            'inst_id' : ['exact', 'in']
        }

class ParameterFilter(FilterSet):
    Field.register_lookup(NotEqual)
    #Field.register_lookup(NotIn)

    class Meta:
        model = Parameter
        fields = {
            #filters:'exact','ne', 'lt', 'gt', 'lte', 'gte', 'in', icontains
            'id': ['exact', 'ne', 'in'], #notin
            'pname': ['exact', 'ne', 'in', 'icontains'], #notin
            'unit': ['exact', 'ne', 'in', 'icontains'], #notin
            'long_name': ['icontains'], 
            'stand_name': ['exact', 'ne', 'in', 'icontains'], #notin 
            'fval_qc': [], 
            'fval': [], 
            'category_long': ['exact', 'ne', 'in', 'icontains'], #notin
            'category_short': ['exact', 'ne', 'in', 'icontains'], #notin
        }

class FerryboxFilter(FilterSet):
    Field.register_lookup(NotEqual)
    #Field.register_lookup(NotIn)

    class Meta:
        model = Ferrybox
        fields = {
            #filters:'exact','ne', 'lt', 'gt', 'lte', 'gte', 'in', icontains
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
            'route_id': ['exact'],
        }