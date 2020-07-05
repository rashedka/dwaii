from django import forms
from django.forms import ModelForm
from .models import medicine, storage


class medicineForm(forms.Form):
    generalName = forms.CharField(max_length=100)
    scientificName = forms.CharField(max_length=100)
    img = forms.ImageField()
