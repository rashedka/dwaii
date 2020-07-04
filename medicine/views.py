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
from .form import medicineForm


def index(request):
    if AnonymousUser.is_authenticated:
        context = {
        }
    else :
        users = user_info.objects.get(username=request.user)
        context = {
            'user': users
        }
    return render(request, 'index.html', context)


def search(request):
    searchword = request.GET['search']
    searchresult = storage.objects.filter(medicine__generalName__icontains=searchword, is_Available=True).order_by('-updateDate').all()
    context = {
        'searchValue': searchword,
        's': searchresult,
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
        if request.POST['password'] == request.POST['password2']:
            user = User.objects.create_user(username, request.POST['email'], password)
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
    if request.method == 'POST':
        medform = medicineForm(request.POST, request.FILES)
        if medform.is_valid():
            med = medicine()
            med.generalName = medform.cleaned_data['generalName']
            med.scientificName = medform.cleaned_data['scientificName']
            med.img = medform.cleaned_data['img']
            med.save()
            return redirect('add_to_storage')
        else:
            msg ='لم يتم اضافة الدواء'
    msg = ''

    context = {
        'form':form,
        'msg': msg,
    }
    return render(request, 'addMedicine.html', context)



def productinfo(request, productId):
    list = storage.objects.get(id=productId)
    user = get_object_or_404(user_info, username=list.username)
    relatesmedlist = storage.objects.filter(medicine__scientificName=list.medicine.scientificName)[:4]

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


def Registerinfo(request):
    if user_info.objects.filter(username=request.user).exists():
        return redirect('profile')
    else:
        return render(request, 'infoRegister.html')


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
    else:
        user_infos = user_info()
        user_infos.pharmacyName = request.POST['pharmacyName']
        user_infos.city = request.POST['city']
        user_infos.location = request.POST['location']
        user_infos.phone_number = request.POST['phoneNumber']
        user_infos.facebookPage = request.POST['facebookpage']
        user_infos.username= user
        user_infos.save()

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
    else :
        redirect('infoRegister')


@login_required(login_url='/medicine/sign/')
def add_to_storage(request):
    user = user_info.objects.get(username=request.user)
    medicines = medicine.objects.all()
    context = {
        'medicine': medicines,
        'use': user,
    }
    return render(request, 'add_to_storage.html', context)


@login_required(login_url='/medicine/sign/')
def add_to_storage_backend(request):
    user = get_object_or_404(User, username=request.user)
    if storage.objects.filter(medicine__generalName=request.POST['med_name'], username=request.user,
                              dose=request.POST['dose']).exists():
        return HttpResponse('الدواء مضاف مسبقا في الصيدلية')

    else:
        if medicine.objects.filter(generalName=request.POST['med_name']).exists():
            medicine_storage_info = get_object_or_404(medicine, generalName=request.POST['med_name'])
        else:
            medicine_storage_info = medicine()
            medicine_storage_info.generalName = request.POST['med_name']
            medicine_storage_info.save()
        medicine_storage = storage()
        medicine_storage.username = user
        medicine_storage.medicine = medicine_storage_info
        medicine_storage.price = request.POST['price']
        medicine_storage.dose = request.POST['dose']
        medicine_storage.is_Available = True
        medicine_storage.save()
        return redirect('profile')

def adminDash(request):

    return render(request, 'adminDashboard.html')
