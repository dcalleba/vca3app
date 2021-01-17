# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
TIME_ZONE = "Europe/Paris"

# Create your models here .

class Visiteur(models.Model):
    pro_id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    page = models.CharField(max_length=40, blank=True, null=True)
    test = models.CharField(max_length=40, blank=True, null=True)
    test2 = models.CharField(max_length=40, blank=True, null=True)
    test3 = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'register_visiteur'



