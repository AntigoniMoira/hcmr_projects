from rest_framework import serializers
from .models import Platform, Institution, Parameter, Ferrybox, ProductRequest
#helps to select fields
from drf_queryfields import QueryFieldsMixin
from django.contrib.auth import get_user_model
from django.db.models import Q

#converts to JSON
#validations for data passed

class PlatformSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Platform
        fields = '__all__'
       
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
        fields = '__all__'

class InstitutionSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Institution
        fields = '__all__'

class ParameterSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Parameter
        fields = '__all__'

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

class NoDvalqcDataSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = None
        fields = ('id', 'dt', 'lat', 'lon', 'posqc', 'pres', 'presqc', 'param', 'val', 'valqc')

class ProductRequestsSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = ProductRequest
        fields = '__all__'