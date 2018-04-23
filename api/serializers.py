from rest_framework import serializers
from .models import Platform, Institution, Parameter, Ferrybox
#helps to select fields
from drf_queryfields import QueryFieldsMixin
from django.contrib.auth import get_user_model

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

class DeepObservAllDataSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = None
        fields = ('id', 'dt', 'lat', 'lon', 'posqc', 'pres', 'presqc', 'param', 'val', 'valqc', 'dvalqc', 'rval', 'rvalqc')

class DeepObservDataSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = None
        fields = ('id', 'dt', 'lat', 'lon', 'posqc', 'pres', 'presqc', 'param', 'val', 'valqc', 'dvalqc', 'rval', 'rvalqc')      
              
    def to_representation(self, obj):
        ret = super(DeepObservDataSerializer, self).to_representation(obj)
        if ret['rvalqc'] != 9:
            ret['val'] = ret['rval']
        ret.pop('rval')
        ret.pop('rvalqc')
        return ret

class FerryboxSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Ferrybox
        fields = ('id', 'dt', 'lat', 'lon', 'posqc', 'pres', 'presqc', 'param', 'val', 'valqc', 'dvalqc', 'route_id')

class InstitutionSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Institution
        fields = ('id', 'name_native', 'abrv', 'country', 'cdf_name')

class ParameterSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Parameter
        fields = ('id', 'pname', 'unit', 'long_name', 'stand_name', 'fval_qc', 'fval', 'category_long', 'category_short')

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    email2 = serializers.EmailField(label='Confirm Email')
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
        ]
        extra_kwargs = {"password":
                            {
                                "write_only": True
                            }

        }

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise serializers.ValidationError("Emails must match!")
        return value

    def create (self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password =  validated_data['password']
        user_obj = User(
            username = username,
            email = email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data
