from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from medicine.models import user_info, medicine, storage, requestMedi, location
from . import form
from django.core.mail import send_mail
from django.conf import settings
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users
from .form import medicineForm, userInfoForm, addToStorageForm, editStorageForm, loginForm, requestMedForm, \
    registerForm, locationForm, contactForm, addBranchForm
from django.db.models import Q


def base_layout(request):
    return render(request, 'index.html')

def privacy(request):
    return render(request, 'privacy.html')

def aboutUs(request):
    return render(request, 'aboutus.html')


def contact(request):
    conForm = contactForm()
    if request.method == 'POST':
        conForm = contactForm(request.POST)
        if conForm.is_valid():
            message = conForm.cleaned_data['message']
            subject = conForm.cleaned_data['subject']
            send_mail(subject,
                      message,
                      settings.EMAIL_HOST_USER,
                      ['dx20112255@gmail.com',
                       'support@dwaiisudan.com'],
                      fail_silently=False)
    context = {
        'form': conForm,
    }
    return render(request, 'contact.html', context)


def index(request):
    user_infos = user_info.objects.all().count() - 3
    medicines = medicine.objects.all().count()
    quantity = storage.objects.all().count()
    context = {
        'user_info': user_infos,
        'medicine': medicines,
        'quantity': quantity,
    }
    if AnonymousUser.is_authenticated:
        pass
    else:
        users = user_info.objects.get(username=request.user)
        context += {
            'user': users
        }
    return render(request, 'index.html', context)


@unauthenticated_user
def sign(request):
    form = loginForm()
    formRegister = registerForm()
    msg1 = ''
    if request.method == 'POST':
        form = loginForm(request.POST)
        formRegister = registerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            result = authenticate(username=username, password=password)
            if result is not None:
                login(request, result)
                return redirect(profile)
            else:
                msg1 = 'يوجد خطأ في إسم المستخدم أو كلمة السر'
        elif formRegister.is_valid():
            username = formRegister.cleaned_data['username2']
            password = formRegister.cleaned_data['password1']
            email = formRegister.cleaned_data['email']
            user = User.objects.create_user(
                username,
                email,
                password, )
            user.first_name = formRegister.cleaned_data['first_name']
            user.last_name = formRegister.cleaned_data['last_name']
            user.save()
            result = authenticate(username=username, password=password)
            if result is not None:
                login(request, result)
                return redirect('infoRegister')

    context = {
        'form': form,
        'formRegister': formRegister,
        'msg1': msg1,

    }
    return render(request, 'sign.html', context)


def allMedicine(request):
    list = storage.objects.all().order_by('medicine__generalName').prefetch_related('username')

    context = {
        'medicineList': list,
    }
    return render(request, 'allMedicine.html', context)


def search(request):
    searchword = request.GET['search']
    searchresult = storage.objects.filter(
        Q(medicine__generalName__icontains=searchword) | Q(
            medicine__scientificName__icontains=searchword) | Q(medicine__arabicName__icontains=searchword),
        is_Available=True).order_by('medicine__generalName', '-updateDate').all().prefetch_related('username')

    if searchresult.exists():
        msg = ""
    else:
        msg = "الدواء غير موجود"
    context = {
        'searchValue': searchword,
        'medicineList': searchresult,
        'msg': msg,
    }
    return render(request, 'allMedicine.html', context)


def addMedicine(request):
    form = medicineForm()
    msg = ''
    if request.method == 'POST':
        medform = medicineForm(request.POST, request.FILES)
        if medform.is_valid():
            med = medicine()
            med.generalName = medform.cleaned_data['generalName']
            med.arabicName = medform.cleaned_data['arabicName']
            med.scientificName = medform.cleaned_data['scientificName']
            med.manufactureCompanyAr = medform.cleaned_data['manufactureCompanyAr']
            med.manufactureCompanyEn = medform.cleaned_data['manufactureCompanyEn']
            med.type = medform.cleaned_data['type']
            med.category = medform.cleaned_data['category']
            med.img = medform.cleaned_data['img']
            med.save()
            msg = 'تمت إضافة دواء : ({}) الى القائمة الرجاء إضافته الى قائمة الأدوية المتوفرة في الصيدلية بعد الإنتهاء ' \
                  'من إضافة الادوية الى القائمة'.format(
                medform.cleaned_data['generalName'])
        else:
            msg = 'لم يتم اضافة الدواء'

    context = {
        'form': form,
        'msg': msg,
    }
    return render(request, 'addMedicine.html', context)


def productinfo(request, productId):
    list = storage.objects.get(id=productId)
    locations = list.username.location_set.all()
    user = get_object_or_404(user_info, username=list.username)
    relatesmedlist = storage.objects.filter(
        medicine__scientificName=list.medicine.scientificName)[:4]

    context = {
        'medicine': list,
        'relatedMeds': relatesmedlist,
        'info': user,
        'location': locations,
    }
    return render(request, 'productinfo.html', context)

def requestinfo(request, requestId):
    list = requestMedi.objects.get(id=requestId)
    locations = list.username.location_set.all()
    user = get_object_or_404(user_info, username=list.username)

    context = {
        'medicine': list,
        'info': user,
        'location': locations,
    }
    return render(request, 'requestinfo.html', context)


def editproduct(request, productId):
    if request.user == storage.objects.get(id=productId).username:
        info = storage.objects.get(id=productId)
        form = editStorageForm(instance=info)
        if request.method == 'POST':
            form = editStorageForm(request.POST, instance=info)
            if form.is_valid():
                form.save()
                return redirect('profile')
            else:
                return HttpResponse('error')
        print(info)
        context = {
            'info': info,
            'form': form,
        }
        return render(request, 'editMed.html', context)
    else:
        return redirect('   profile')


def editproductBackend(request, productId):
    if request.user == storage.objects.get(id=productId).username:
        info = storage.objects.get(id=productId)
        info.price = request.POST['price']
        info.is_Available = request.POST['available']
        info.save()
        return redirect(profile)
    else:
        return HttpResponse('error')


@login_required(login_url='/medicine/sign/')
def Registerinfo(request):
    locForm = ''
    if user_info.objects.filter(username=request.user).exists():
        form = userInfoForm(instance=user_info.objects.get(username=request.user))
        users =request.user
    else:
        form = userInfoForm()
        locForm = locationForm()
        users = ''
        if request.method == 'POST':
            form = userInfoForm(request.POST)
            locForm = locationForm(request.POST)
            if form.is_valid() & locForm.is_valid():
                userInfo = user_info()
                locInof = location()
                userInfo.username = request.user
                userInfo.pharmacyName = form.cleaned_data['pharmacyName']
                userInfo.accType = form.cleaned_data['accType']
                userInfo.phone_number = form.cleaned_data['phone_number']
                userInfo.facebookPage = form.cleaned_data['facebookPage']
                userInfo.whatsappNumber = form.cleaned_data['whatsappNumber']
                userInfo.save()

                locInof.username = request.user
                locInof.city = locForm.cleaned_data['city']
                locInof.location = locForm.cleaned_data['location']
                locInof.save()
                return redirect('profile')

    context = {
        'form': form,
        'locForm': locForm,
        'users': users,
    }
    return render(request, 'infoRegister.html', context)


@login_required(login_url='/medicine/sign/')
def logout_backend(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/medicine/sign/')
def profile(request):
    if user_info.objects.filter(username=request.user).exists():
        user = get_object_or_404(User, username=request.user)
        user_infos = get_object_or_404(user_info, username=request.user)
        medicines = user.storage_set.all()

        myFilter = OrderFilter(request.GET, queryset=medicines)
        medicines = myFilter.qs

        context = {
            'medicine': medicines,
            'user': user_infos,
            'myFilter': myFilter,
        }
        return render(request, 'profile.html', context)
    else:
        return redirect('infoRegister')

def visitorProfile(request, phUrl):
    user_infos = get_object_or_404(user_info, username__id=phUrl)
    user = get_object_or_404(User, id=phUrl)

    medicines = user.storage_set.all()

    context = {
        'medicine': medicines,
        'user': user_infos,
    }
    return render(request, 'profilev.html', context)


@login_required(login_url='/medicine/sign/')
def add_to_storage(request):
    user = get_object_or_404(user_info, username=request.user)
    medicines = medicine.objects.all()
    form = addToStorageForm()
    msg = ''
    if request.method == 'POST':
        storageForm = addToStorageForm(request.POST, request.FILES)
        if storageForm.is_valid():
            storages = storage()
            storages.username = request.user
            storages.medicine = storageForm.cleaned_data['medicine']
            storages.dose = storageForm.cleaned_data['dose']
            storages.price = storageForm.cleaned_data['price']
            storages.is_Available = True

            storages.save()
            msg = 'تمت إضافة دواء : {}'.format(
                storageForm.cleaned_data['medicine'])
        else:
            msg = 'لم يتم اضافة الدواء'

    context = {
        'form': form,
        'medicine': medicines,
        'msg': msg,
        'user': user,
    }
    return render(request, 'add_to_storage.html', context)


@allowed_users('admin')
def adminDash(request):
    medicines = medicine.objects.all()
    user_infos = user_info.objects.all().count() - 3
    medicinesc = medicine.objects.all().count()
    quantity = storage.objects.all().count()
    context = {
        'medicine': medicines,
        'medicinec': medicinesc,
        'quantity': quantity,
        'user_info': user_infos,
    }
    return render(request, 'adminDashboard.html', context)


def requestMedicine(request):
    user = get_object_or_404(user_info, username=request.user)
    if user.accType == 'no':
        form = requestMedForm()
        msg = ''
        if request.method == 'POST':
            requestForm = requestMedForm(request.POST, request.FILES)
            if requestForm.is_valid():
                requrstModel = requestMedi()
                requrstModel.username = request.user
                requrstModel.medicineGeneral = requestForm.cleaned_data['medicineGeneral']
                requrstModel.type = requestForm.cleaned_data['type']
                requrstModel.img = requestForm.cleaned_data['img']
                requrstModel.description = requestForm.cleaned_data['description']
                requrstModel.prescription = requestForm.cleaned_data['prescription']
                requrstModel.save()
                if requestForm.cleaned_data['type'] == 'request':
                    msg = 'تمت إضافة الدواء الى قائمة الأدوية المطلوبة : {}'.format(
                        requestForm.cleaned_data['medicineGeneral'])
                else:
                    msg = 'تمت إضافة الدواء الى قائمة الأدوية المتبرع بها : {}'.format(
                        requestForm.cleaned_data['medicineGeneral'])
            else:
                msg = 'لم يتم اضافة الدواء'

        context = {
            'form': form,
            'msg': msg,
        }
        return render(request, 'requestMedicine.html', context)
    else:
        return redirect('index')


def requestList(request):
    list = requestMedi.objects.all().order_by('requestDate').filter(type='request')
    context = {
        'medicineList': list,
    }
    return render(request, 'allRequest.html', context)

def searchRequest(request):
    searchword = request.GET['search']
    searchresult = requestMedi.objects.filter(medicineGeneral__icontains=searchword, type='request').order_by('medicineGeneral', '-requestDate').all()

    if searchresult.exists():
        msg = ""
    else:
        msg = "الدواء غير موجود"
    context = {
        'searchValue': searchword,
        'medicineList': searchresult,
        'msg': msg,
    }
    return render(request, 'allRequest.html', context)

def donateList(request):
    list = requestMedi.objects.all().order_by('requestDate').filter(type='donate')
    context = {
        'medicineList': list,
    }
    return render(request, 'alldonate.html', context)

def searchdonate(request):
    searchword = request.GET['search']
    searchresult = requestMedi.objects.filter(medicineGeneral__icontains=searchword, type='donate').order_by('medicineGeneral', '-requestDate').all()

    if searchresult.exists():
        msg = ""
    else:
        msg = "الدواء غير موجود"
    context = {
        'searchValue': searchword,
        'medicineList': searchresult,
        'msg': msg,
    }
    return render(request, 'alldonate.html', context)

def addBranch(request):
    forms = addBranchForm()
    msg =''
    if request.method == 'POST':
        forms = addBranchForm(request.POST)
        if forms.is_valid():
            locations = location()
            locations.username = request.user
            locations.city = forms.cleaned_data['city']
            locations.location = forms.cleaned_data['location']
            locations.save()
            msg = 'تمت إضافة الفرع'
    context = {
        'form': forms,
        'msg': msg,
    }
    return render(request, "addbranch.html", context)
