from rest_framework import serializers
from .models import Platform, Institution, Parameter
#helps to select fields
from drf_queryfields import QueryFieldsMixin
from django.contrib.auth import get_user_model
from django.db.models import Q

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

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(label='Email Address')
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

    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email2")
        email2 = value
        if email1 != email2:
            raise serializers.ValidationError("Emails must match!")
        
        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise serializers.ValidationError("This user has already registered.")

        return value

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

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_blank=True, read_only=True)
    email = serializers.EmailField(label='Email Address', required=False, allow_blank=True)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]

    def validate(self, data):
        user_obj = None
        email = data.get("email", None)
        password = data["password"]

        user = User.objects.filter(email=email).distinct()
        user=user.exclude(email__isnull=True).exclude(email='')
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError("This email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Incorect credentials please try again.")
                
        data['username']=user_obj.username
        return data

