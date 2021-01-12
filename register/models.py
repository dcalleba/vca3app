# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
TIME_ZONE = "Europe/Paris"

# Create your models here .

class Visiteur(models.Model):
	pro_id = models.AutoField(primary_key=True)
	ip = models.CharField(max_length=40,default='',verbose_name="IP")
	email = models.EmailField(max_length=40,default='', blank=False,verbose_name="Email   ")
	page =models.CharField(max_length=40,default='',verbose_name="Page")
	#date_creation = models.DateTimeField(default=timezone.now(), blank=True, verbose_name="Date de Création")
	test = models.CharField(max_length=40,default='',verbose_name="Test")
	test2 = models.CharField(max_length=40,default='',verbose_name="Test")

	test3 = models.CharField(max_length=40,default='',verbose_name="Test")
	
	
	def __str__(self):
		""" 
		Cette méthode que nous définirons dans tous les modèles
		nous permettra de reconnaître facilement les différents objets que 
		nous traiterons plus tard et dans l'administration
		"""
		return self.email


