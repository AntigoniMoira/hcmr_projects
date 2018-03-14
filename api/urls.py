from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^help', views.help, name='help'),
    #url(r'^(?P<platform>\w+)/',views.platforms_data,name='platforms_data'),
    url(r'^platforms/', views.PlatformList.as_view(),name='platform_list'),
    url(r'^institutions/', views.InstitutionList.as_view(),name='institution_list'),
    url(r'^parameters/', views.ParameterList.as_view(),name='parameter_list'),
    url(r'^(?P<platform>\w+)/', views.DataList.as_view(),name='data_list'),
    
]