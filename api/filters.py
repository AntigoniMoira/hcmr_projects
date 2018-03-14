from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django_filters import rest_framework as filters
from distutils.util import strtobool
from .models import Platform, Institution, Parameter
from django import forms
#imports for custom lookups
from .lookups import NotEqual
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
            'id': ['exact', 'in','ne'],
            'pid': ['exact', 'ne','in'],
            'tspr': ['exact', 'ne'],
            'type': ['exact', 'ne', 'in'],
            'inst': ['exact'], #einai kai kleidi gia institutions opote ftiaxnei drop down me ta institutions
            'inst__id': ['exact', 'in'],
            'dts': [ 'lt', 'gt', 'lte', 'gte', 'icontains'],
            'dte': [ 'lt', 'gt', 'lte', 'gte', 'icontains'],
            'lat':  ['lt', 'gt', 'lte', 'gte'],
            'lon':  ['lt', 'gt', 'lte', 'gte'],
            'status': [],
            'params' : ['icontains'], 
            'platform_code': ['exact', 'ne'],
            'wmo': ['exact', 'ne', 'icontains'],
            'pi_name' : ['icontains'], 
            #'author' : ['icontains'],
            #'contact' : ['icontains'],
            #'island': [],
            #'pl_name' : [],
            #'inst_ref' : [],
            'assembly_center' : ['exact', 'ne', 'in'],
            #'site_code' : [],
            #'source' : []

        }

class DataFilter(FilterSet):
    #Field.register_lookup(NotEqual)
    #Field.register_lookup(NotIn)

    class Meta:
        model = None
        fields = {
            #filters:'exact','ne', 'lt', 'gt', 'lte', 'gte', 'in', icontains
            'id': ['exact', 'in'],
            #'pid': ['exact', 'ne','in'],
            
        }

class InstitutionFilter(FilterSet):
    Field.register_lookup(NotEqual)
    #Field.register_lookup(NotIn)

    class Meta:
        model = Institution
        fields = {
            #filters:'exact','ne', 'lt', 'gt', 'lte', 'gte', 'in', icontains
            'id': ['exact', 'in'],
            'name_native' : [],
            'abrv' : [],
            'country' : [],
            'cdf_name' : [] 
        }

class ParameterFilter(FilterSet):
    Field.register_lookup(NotEqual)
    #Field.register_lookup(NotIn)

    class Meta:
        model = Parameter
        fields = {
            #filters:'exact','ne', 'lt', 'gt', 'lte', 'gte', 'in', icontains
            'id': ['exact', 'in'],
            'pname': [],
            'unit': [], 
            'long_name': [], 
            'stand_name': [], 
            'fval_qc': [], 
            'fval': [], 
            'category_long': [], 
            'category_short': []
        }