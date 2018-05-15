from __future__ import unicode_literals
from django.db.models.base import ModelBase

from django.db import models


class Institution(models.Model):
    name_native = models.CharField(max_length=100)
    abrv = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    cdf_name = models.CharField(max_length=100)

    class Meta:
        # No database table creation or deletion operations will be performed for this model.
        managed = False
        ordering = ('id', )
        db_table = 'metadata\".\"institutions'

    def __str__(self):
        return self.name_native


class Platform(models.Model):
    pid = models.CharField(unique=True, max_length=100)
    tspr = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    # many-to-one relationship
    inst = models.ForeignKey(Institution, default='1',
                             db_column='inst', to_field='id', on_delete=models.CASCADE)
    dts = models.CharField(max_length=100)
    dte = models.CharField(max_length=100)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    status = models.BooleanField()
    params = models.CharField(max_length=100)
    platform_code = models.CharField(max_length=100)
    wmo = models.CharField(max_length=100)
    pi_name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    island = models.BooleanField()
    pl_name = models.CharField(max_length=100)
    inst_ref = models.CharField(max_length=100)
    assembly_center = models.CharField(max_length=100)
    site_code = models.CharField(max_length=100)
    source = models.CharField(max_length=100)

    class Meta:
        # No database table creation or deletion operations will be performed for this model.
        managed = False
        ordering = ('id', )
        verbose_name_plural = 'platforms'
        db_table = 'metadata\".\"platforms'

    def __str__(self):
        return self.pid


class Parameter(models.Model):
    pname = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    long_name = models.CharField(max_length=100)
    stand_name = models.CharField(max_length=100)
    fval_qc = models.ImageField()
    fval = models.FloatField(blank=True, null=True)
    category_long = models.CharField(max_length=100)
    category_short = models.CharField(max_length=100)

    class Meta:
        # No database table creation or deletion operations will be performed for this model.
        managed = False
        ordering = ('id', )
        db_table = 'metadata\".\"parameters'

    def __str__(self):
        return self.pname


def getModel():
    class MyClassMetaclass(models.base.ModelBase):
        def __new__(cls, name, bases, attrs):
            #name += db_table
            return models.base.ModelBase.__new__(cls, name, bases, attrs)

    class MyClass(models.Model):
        __metaclass__ = MyClassMetaclass

        #pid = models.ForeignKey(Platform, db_column='pid', to_field='id', null=False)
        dt = models.DateTimeField(blank=True, null=True)
        lat = models.TextField()
        lon = models.TextField()
        posqc = models.SmallIntegerField(blank=True, null=True, default='0')
        pres = models.TextField()
        presqc = models.SmallIntegerField(blank=True, null=True, default='0')
        param = models.ForeignKey(
            Parameter, db_index=True, db_column='param', to_field='id', null=False, on_delete=models.CASCADE,)
        val = models.FloatField(blank=True, null=True)
        valqc = models.SmallIntegerField(blank=True, null=True, default='0')
        dvalqc = models.SmallIntegerField(blank=True, null=True)

        class Meta:
            # No database table creation or deletion operations will be performed for this model.
            managed = False
            ordering = ('id', )

    return MyClass

def DeepObservgetModel():
    class DeepObservMyClassMetaclass(models.base.ModelBase):
        def __new__(cls, name, bases, attrs):
            #name += db_table
            return models.base.ModelBase.__new__(cls, name, bases, attrs)

    class DeepObservMyClass(models.Model):
        __metaclass__ = DeepObservMyClassMetaclass

        #pid = models.ForeignKey(Platform, db_column='pid', to_field='id', null=False)
        dt = models.DateTimeField(blank=True, null=True)
        lat = models.TextField()
        lon = models.TextField()
        posqc = models.SmallIntegerField(blank=True, null=True, default='0')
        pres = models.TextField()
        presqc = models.SmallIntegerField(blank=True, null=True, default='0')
        param = models.ForeignKey(
            Parameter, db_index=True, db_column='param', to_field='id', null=False, on_delete=models.CASCADE,)
        val = models.FloatField(blank=True, null=True)
        valqc = models.SmallIntegerField(blank=True, null=True, default='0')
        dvalqc = models.SmallIntegerField(blank=True, null=True)
        rval = models.FloatField(blank=True, null=True)
        rvalqc = models.SmallIntegerField(blank=True, null=True, default='0')

        class Meta:
            # No database table creation or deletion operations will be performed for this model.
            managed = False
            ordering = ('id', )

    return DeepObservMyClass


class Ferrybox(models.Model):
    pid = models.ForeignKey(Platform, default='1757',
                            db_column='pid', to_field='id', null=False, on_delete=models.CASCADE,)
    dt = models.DateTimeField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    posqc = models.SmallIntegerField(blank=True, null=True, default='0')
    pres = models.FloatField(blank=True, null=True)
    presqc = models.SmallIntegerField(blank=True, null=True, default='0')
    param = models.ForeignKey(
        Parameter, db_column='param', to_field='id', null=False, on_delete=models.CASCADE,)
    val = models.FloatField(blank=True, null=True)
    valqc = models.SmallIntegerField(blank=True, null=True, default='0')
    dvalqc = models.SmallIntegerField(blank=True, null=True)
    route_id = models.IntegerField(blank=True, null=True)

    class Meta:
        # No database table creation or deletion operations will be performed for this model.
        managed = False
        ordering = ('id',)
        verbose_name_plural = 'Ferrybox'
        db_table = 'data\".\"TS_FB_SAEG01'

    def __str__(self):
        return str(self.pid)

def getModel_no_dvalqc():
    class MyClassMetaclass(models.base.ModelBase):
        def __new__(cls, name, bases, attrs):
            #name += db_table
            return models.base.ModelBase.__new__(cls, name, bases, attrs)

    class MyClass(models.Model):
        __metaclass__ = MyClassMetaclass

        #pid = models.ForeignKey(Platform, db_column='pid', to_field='id', null=False)
        dt = models.DateTimeField(blank=True, null=True)
        lat = models.TextField()
        lon = models.TextField()
        posqc = models.SmallIntegerField(blank=True, null=True, default='0')
        pres = models.TextField()
        presqc = models.SmallIntegerField(blank=True, null=True, default='0')
        param = models.ForeignKey(
            Parameter, db_index=True, db_column='param', to_field='id', null=False, on_delete=models.CASCADE,)
        val = models.FloatField(blank=True, null=True)
        valqc = models.SmallIntegerField(blank=True, null=True, default='0')
    
        class Meta:
            # No database table creation or deletion operations will be performed for this model.
            managed = False
            ordering = ('dt','pres', 'param__id')

    return MyClass

class Request(models.Model):
    platform = models.TextField(null=False)
    querystring = models.TextField(null=False)
    
    class Meta:
        # No database table creation or deletion operations will be performed for this model.
        managed = False
        ordering = ('-id',)
        verbose_name_plural = 'Request'
        db_table = 'uman\".\"requests'

class Product(models.Model):
    file_path = models.TextField(null=False)
    creation_date = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        # No database table creation or deletion operations will be performed for this model.
        managed = False
        ordering = ('-id',)
        verbose_name_plural = 'Product'
        db_table = 'uman\".\"products'

class ProductRequest(models.Model):
    product_id = models.ForeignKey(Product, default='1',
                             db_column='product_id', to_field='id', on_delete=models.CASCADE)
    request_id = models.ForeignKey(Request, default='1',
                             db_column='request_id', to_field='id', on_delete=models.CASCADE)
    
    class Meta:
        # No database table creation or deletion operations will be performed for this model.
        managed = False
        ordering = ('-product_id', '-request_id',)
        verbose_name_plural = 'ProductRequest'
        db_table = 'uman\".\"product_requests'