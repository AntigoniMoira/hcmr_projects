"""hcmr_poseidon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login 
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
admin.autodiscover()

schema_view = get_schema_view(
    openapi.Info(
        title="HCMR API",
        default_version='v1',
        description="Test description",
    ),
    #validators=['flex', 'ssv'],
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger',
                                           cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc',
                                         cache_timeout=0), name='schema-redoc'),
    url(r'^api/', include('api.urls')),
    #url(r'^accounts/login/$',login, {'template_name': 'api/login.html'}),
]
