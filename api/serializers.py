from rest_framework import serializers
from .models import Platform, Institution, Parameter
#helps to select fields
from drf_queryfields import QueryFieldsMixin

#converts to JSON
#validations for data passed

class PlatformSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Platform
        fields = ('id', 'pid', 'tspr', 'type', 'inst', 'dts', 'dte', 'lat', 'lon', 'status', 'params', 'platform_code', 'wmo',
                    'pi_name', 'author', 'contact', 'island', 'pl_name', 'inst_ref', 'assembly_center', 'site_code', 'source')

class DataSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = None
        fields = ('id', 'dt', 'lat', 'lon', 'posqc', 'pres', 'presqc', 'param', 'val', 'valqc', 'dvalqc')

class InstitutionSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Institution
        fields = ('id', 'name_native', 'abrv', 'country', 'cdf_name')

class ParameterSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Parameter
        fields = ('id', 'pname', 'unit', 'long_name', 'stand_name', 'fval_qc', 'fval', 'category_long', 'category_short')