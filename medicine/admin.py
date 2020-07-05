from django.contrib import admin

# Register your models here.
from medicine.models import storage, medicine, user_info

admin.site.register(user_info)
admin.site.register(medicine)
admin.site.register(storage)
