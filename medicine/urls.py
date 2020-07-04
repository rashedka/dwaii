from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from medicine.views import search, allMedicine, user_login_backend, sign, logout_backend, user_register_backend, \
    profile, add_to_storage, add_to_storage_backend, productinfo, Registerinfo, RegisterinfoBackend, editproduct, \
    editproductBackend, addMedicine

urlpatterns = [
    path('search', search, name='search'),
    path('sign/', sign, name='sign'),
    path('', allMedicine, name='allMedicine'),
    path('sign/user_login_backend/', user_login_backend, name='user_login_backend'),
    path('sign/user_register_backend/', user_register_backend, name='user_register_backend'),
    path('profile/add_to_storage/', add_to_storage, name='add_to_storage'),
    path('profile/addMedicine/', addMedicine, name='addMedicine'),
    path('profile/add_to_storage_backend/', add_to_storage_backend, name='add_to_storage_backend'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_backend, name='logout'),
    path('info/<int:productId>', productinfo, name='productinfo'),
    path('info/edit/<int:productId>', editproduct, name='editproduct'),
    path('info/editBackend/<int:productId>', editproductBackend, name='editproductBackend'),
    path('profile/inforegister', Registerinfo, name='infoRegister'),
    path('profile/inforegisterbackend', RegisterinfoBackend, name='inforegisterbackend'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
