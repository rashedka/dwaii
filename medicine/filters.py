import django_filters
from django import forms

from .models import *

class OrderFilter(django_filters.FilterSet):

    class Meta:
        model = storage
        fields = ['medicine']

        labels = {
            'medicine': 'إسم الدواء',
        }



