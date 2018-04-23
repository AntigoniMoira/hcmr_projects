from django.contrib import admin
from .models import Platform, Institution, Parameter, Ferrybox
# Register your models here.

class PlatformAdmin(admin.ModelAdmin):
    list_display = ['id', 'pid', 'tspr', 'type', 'platform_code']
    search_fields = ['id', 'pid', 'tspr', 'type', 'platform_code']
    list_per_page =10

admin.site.register(Platform, PlatformAdmin)

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_native', 'abrv', 'country', 'cdf_name']
    search_fields = ['id', 'name_native', 'abrv', 'country', 'cdf_name']
    list_per_page=10

admin.site.register(Institution, InstitutionAdmin)

class ParameterAdmin(admin.ModelAdmin):
    list_display = ['id', 'pname', 'unit', 'stand_name', 'category_short']
    search_fields = ['id',  'pname', 'unit', 'stand_name', 'category_short']
    list_per_page=10

admin.site.register(Parameter, ParameterAdmin)

class FerryboxAdmin(admin.ModelAdmin):
    list_display = ['id', 'dt', 'lat', 'lon', 'pres', 'param', 'val']
    search_fields = ['id', 'dt', 'lat', 'lon', 'pres', 'param', 'val']
    list_per_page=10

admin.site.register(Ferrybox, FerryboxAdmin)

