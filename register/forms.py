# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.core.exceptions import ValidationError
from .models import Visiteur

class VisiteurForm(forms.ModelForm):
	class Meta :
		model = Visiteur
		fields = '__all__'
		exclude = ['ip','page','date_creation','test','test2','test3']
		
	def __init__(self, *args, **kwargs):
		super(VisiteurForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
  

# class VisiteurFormDate(forms.ModelForm):
# 	class Meta :
# 		model = Visiteur
# 		fields = '__all__'
# 		#exclude = ['date_creation','test2','test3']
		
# 	def __init__(self, *args, **kwargs):
# 		super(VisiteurFormDate, self).__init__(*args, **kwargs) # Call to ModelForm constructor
		
