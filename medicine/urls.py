from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from medicine.views import search, allMedicine, user_login_backend, sign, logout_backend, user_register_backend, \
    profile, add_to_storage, productinfo, Registerinfo, RegisterinfoBackend, editproduct, \
    editproductBackend, addMedicine
from django.contrib.auth import views as auth_views

urlpatterns = [
                  path('search', search, name='search'),
                  path('sign/', sign, name='sign'),
                  path('', allMedicine, name='allMedicine'),
                  path('sign/user_login_backend/', user_login_backend, name='user_login_backend'),
                  path('sign/user_register_backend/', user_register_backend, name='user_register_backend'),
                  path('profile/add_to_storage/', add_to_storage, name='add_to_storage'),
                  path('profile/addMedicine/', addMedicine, name='addMedicine'),
                  path('profile/', profile, name='profile'),
                  path('logout/', logout_backend, name='logout'),
                  path('info/<int:productId>', productinfo, name='productinfo'),
                  path('info/edit/<int:productId>', editproduct, name='editproduct'),
                  path('info/editBackend/<int:productId>', editproductBackend, name='editproductBackend'),
                  path('profile/inforegister', Registerinfo, name='infoRegister'),
                  path('profile/inforegisterbackend', RegisterinfoBackend, name='inforegisterbackend'),

                  # reset password
                  path('reset_password', auth_views.PasswordResetView.as_view(template_name= "resetPassword.html"), name='reset_password'),
                  path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),
                  path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

