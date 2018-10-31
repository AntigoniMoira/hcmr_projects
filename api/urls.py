from django.conf.urls import url
#from rest_framework_swagger.views import get_swagger_view
from . import views
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    #url(r'^$', schema_view),
    #url(r'^docs/', include_docs_urls(title='My API title')),
    # an example resource endpoint
    #url(r'^hello', views.ApiEndpoint.as_view()),
    # data urls
    url(r'^platforms/', views.PlatformList.as_view(), name='platform_list'),
    url(r'^institutions/', views.InstitutionList.as_view(),
        name='institution_list'),
    url(r'^cdf_institutions/', views.Cdf_InstitutionList.as_view(),
        name='cdf_institution_list'),
    url(r'^parameters/', views.ParameterList.as_view(), name='parameter_list'),
    url(r'^deep_observ/(?P<platform>\w+)/', views.DeepObservDataList.as_view(),name='deep_observ_data_list'),
    # deep_observ_all to return rval and rvalqc
    url(r'^deep_observ_all/(?P<platform>\w+)/', views.DeepObservAllDataList.as_view(),name='deep_observ_all_data_list'),
    url(r'^ferrybox/', views.FerryboxDataList.as_view(),
        name='ferrybox_data_list'),
    url(r'^data/(?P<platform>\w+)/',
        views.DataList.as_view({'get': 'list'}), name='data_list'),
    # excel_service urls
    url(r'^poseidon_platforms_with_measurements_between',
        views.poseidon_platforms_with_measurements_between, name='poseidon_platforms_with_measurements_between'),
    url(r'^poseidon_platform_parameters_with_measurements_between',
        views.poseidon_platform_parameters_with_measurements_between, name='poseidon_platform_parameters_with_measurements_between'),
    #url(r'^poseidon_db_list/(?P<platform>\w+)/',
        #views.Poseidon_db_List.as_view(), name='poseidon_db_list'),
    url(r'^poseidon_db_unique_dt/', views.poseidon_db_unique_dt,
        name='poseidon_db_unique_dt'),
    # online_data service urls
    url(r'^latest_ts/(?P<platform>\w+)/',
        views.ts_latest_data, name='ts_latest_data'),
    url(r'^latest_pr/(?P<platform>\w+)/',
        views.pr_latest_data, name='pr_latest_data'),
    url(r'^online_data_from_mv/',
        views.OnlineDataList.as_view(), name='online_data_list'),

]
