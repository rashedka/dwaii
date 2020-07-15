from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from medicine.models import user_info, medicine, storage
from . import form
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users
from .form import medicineForm, userInfoForm, addToStorageForm
from django.db.models import Q


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


def search(request):
    searchword = request.GET['search']
    searchresult = storage.objects.filter(
        Q(medicine__generalName__icontains=searchword) | Q(
            medicine__scientificName__icontains=searchword),
        is_Available=True).order_by('medicine__generalName', '-updateDate').all()
    if searchresult.exists():
        msg = ""
    else:
        msg = "الدواء غير موجود"
    context = {
        'searchValue': searchword,
        's': searchresult,
        'msg': msg,
    }
    return render(request, 'search.html', context)


@unauthenticated_user
def sign(request):
    return render(request, 'sign.html')


@unauthenticated_user
def user_login_backend(request):
    user = request.POST['username']
    password = request.POST['password']
    result = authenticate(username=user, password=password)
    if result is not None:
        print('login')
        login(request, result)
        link = '/'
        return HttpResponseRedirect(link)
    else:
        return HttpResponse('user is not exist')


@unauthenticated_user
def user_register_backend(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        msg = ''
        if User.objects.filter(email=email).exists():
            msg = 'الايميل مستخدم'
        else:
            if request.POST['password'] == request.POST['password2']:
                user = User.objects.create_user(
                    username,
                    email,
                    password,)
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.save()
                result = authenticate(username=username, password=password)
                if result is not None:
                    login(request, result)
                    return HttpResponseRedirect('/medicine/profile/inforegister')
            elif request.POST['password'] != request.POST['password2']:
                msg = 'الباسوورد غير متطابق'
        return render(request, 'sign.html', {'msg': msg})
    except:
        return HttpResponse('user name is already exist')


def allMedicine(request):
    list = storage.objects.all().order_by('medicine__generalName')
    context = {
        'medicineList': list,
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
            med.scientificName = medform.cleaned_data['scientificName']
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
    user = get_object_or_404(user_info, username=list.username)
    relatesmedlist = storage.objects.filter(
        medicine__scientificName=list.medicine.scientificName)[:4]

    context = {
        'medicine': list,
        'relatedMeds': relatesmedlist,
        'info': user,
    }
    return render(request, 'productinfo.html', context)


def editproduct(request, productId):
    if request.user == storage.objects.get(id=productId).username:
        info = storage.objects.get(id=productId)
        print(info)
        context = {
            'info': info,
        }
        return render(request, 'editMed.html', context)
    else:
        return redirect('profile')


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
    if user_info.objects.filter(username=request.user).exists():
        user_infos = user_info.objects.get(username=request.user.id)
        form = userInfoForm(instance=user_infos)
    else:
        form = userInfoForm()
    context = {
        'form': form,
    }
    return render(request, 'infoRegister.html', context)


@login_required(login_url='/medicine/sign/')
def RegisterinfoBackend(request):
    user = request.user
    if user_info.objects.filter(username=user).exists():
        user_infos = get_object_or_404(user_info, username=user)
        if request.POST['pharmacyName'] != '':
            user_infos.pharmacyName = request.POST['pharmacyName']
        if request.POST['city'] != '':
            user_infos.city = request.POST['city']
        if request.POST['location'] != '':
            user_infos.location = request.POST['location']
        if request.POST['phoneNumber'] != '':
            user_infos.phone_number = request.POST['phoneNumber']
        user_infos.save()
        return redirect('profile')
    else:
        if request.method == 'POST':
            infoform = userInfoForm(request.POST)
            if infoform.is_valid():
                userInfo = user_info()
                userInfo.username = request.user
                userInfo.location = infoform.cleaned_data['location']
                userInfo.pharmacyName = infoform.cleaned_data['pharmacyName']
                userInfo.phone_number = infoform.cleaned_data['phone_number']
                userInfo.facebookPage = infoform.cleaned_data['facebookPage']
                userInfo.city = infoform.cleaned_data['city']
                userInfo.is_pharmacy = infoform.cleaned_data['is_pharmacy']
                userInfo.whatsappNumber = infoform.cleaned_data['whatsappNumber']
                userInfo.save()
                return redirect('profile')
            else:
                return HttpResponse('error')
    return redirect('profile')


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


@login_required(login_url='/medicine/sign/')
def add_to_storage(request):
    user = user_info.objects.get(username=request.user)
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
