from rest_framework import serializers
from .models import Platform, Institution, Parameter, Ferrybox, Cdf_Institution, UserProfile, OnlineData
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

class Cdf_InstitutionSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Cdf_Institution
        fields = '__all__'

class ParameterSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Parameter
        fields = '__all__'

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    firstname = serializers.CharField(allow_blank=False)
    lastname = serializers.CharField(allow_blank=False)
    country = serializers.CharField(allow_blank=False)
    institution = serializers.CharField(allow_blank=True)
    phone = serializers.CharField(allow_blank=False)
    email = serializers.EmailField(label='Email Address')
    password2 = serializers.CharField(allow_blank=False)
    description = serializers.CharField(allow_blank=False)
    class Meta:
        model = User
        fields = [
            'firstname',
            'lastname',
            'country',
            'institution',
            'phone',
            'email',
            'password',
            'password2',
            'description',
        ]
        extra_kwargs = {"password":
                            {
                                "write_only": True
                            },
                        "password2":
                            {
                                "write_only": True
                            }
        }

    def validate(self, data):
        email = data.get('email', None)
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise serializers.ValidationError("This email is already used.")
        password1 = data.get("password")
        password2 = data.get("password2")
        if password1 != password2:
            raise serializers.ValidationError("Passwords must match!")
        return data


    def create (self, validated_data):
        username = validated_data['email']
        email = validated_data['email']
        password =  validated_data['password2']
        user_obj = User(
            username = username,
            email = email,
            is_active = False,
        )
        user_obj.set_password(password)
        user_obj.first_name=validated_data['firstname']
        user_obj.last_name=validated_data['lastname']
        user_obj.save()
        institution=validated_data['institution']
        description=validated_data['description']
        phone=validated_data['phone']
        country=validated_data['country']
        profile = UserProfile.objects.create(user=user_obj, userPhone=phone, country=country, institution=institution, description=description)
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
            if user_obj.is_active==False:
                raise serializers.ValidationError("Your account has not yet been activated.")
                
        data['username']=user_obj.username
        return data

class NoDvalqcDataSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = None
        fields = ('id', 'dt', 'lat', 'lon', 'posqc', 'pres', 'presqc', 'param', 'val', 'valqc')

class OnlineDataSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = OnlineData
        fields = '__all__'