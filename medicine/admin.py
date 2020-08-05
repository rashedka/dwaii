from unicodedata import category

from django.contrib import admin

# Register your models here.
from medicine.models import storage, medicine, user_info, requestMedi, location, medType, medCategory

admin.site.register(user_info)
admin.site.register(medicine)
admin.site.register(storage)
admin.site.register(requestMedi)
admin.site.register(medType)
admin.site.register(medCategory)
admin.site.register(location)

