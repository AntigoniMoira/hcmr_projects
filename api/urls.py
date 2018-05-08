from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index$', views.index, name='index'),
    url(r'^help', views.help, name='help'),
    #user_authentication urls
    url(r'^register/', views.UserCreateAPIView.as_view(), name='register'),
    url(r'^login/', views.UserLoginAPIView.as_view(), name='login'),
    url(r'^logout/', views.logout_user, name='logout'),
    #data urls
    url(r'^platforms/', views.PlatformList.as_view(),name='platform_list'),
    url(r'^institutions/', views.InstitutionList.as_view(),name='institution_list'),
    url(r'^parameters/', views.ParameterList.as_view(),name='parameter_list'),
    url(r'^deep_observ/(?P<platform>\w+)/', views.DeepObservDataList.as_view(),name='deep_observ_data_list'),
    #deep_observ_all to return rval and rvalqc
    url(r'^deep_observ_all/(?P<platform>\w+)', views.DeepObservAllDataList.as_view(),name='deep_observ_all_data_list'),
    url(r'^ferrybox/', views.FerryboxDataList.as_view(),name='ferrybox_data_list'),
    url(r'^data/(?P<platform>\w+)/', views.DataList.as_view(),name='data_list'),
    # excel_service urls
    url(r'^poseidon_platforms_with_measurements_between',  
            views.poseidon_platforms_with_measurements_between, name='poseidon_platforms_with_measurements_between'),
    url(r'^poseidon_platform_parameters_with_measurements_between',  
            views.poseidon_platform_parameters_with_measurements_between, name='poseidon_platform_parameters_with_measurements_between'),
    
]