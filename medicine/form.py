from django import forms
from django.contrib.auth.models import User

from .models import medicine, storage, user_info, location, requestMedi, pharmacyAcc, CustomerAcc, organizationAcc


class medicineForm(forms.ModelForm):
    class Meta:
        model = medicine
        fields = '__all__'
        labels = {
            'generalName': '',
            'arabicName': '',
            'scientificName': '',
            'manufactureCompanyAr': '',
            'manufactureCompanyEn': '',
            'img': 'صورة الدواء :',
            'type': 'نوع الدواء :',
            'category': 'تصنيف الدواء :',
        }
        widgets = {
            'generalName': forms.TextInput(
                attrs={'class': 'form-control col-md-3', 'placeholder': 'الاسم التجاري باللغة الإنجليزية'}),
            'scientificName': forms.TextInput(
                attrs={'class': 'form-control col-md-3 mb-3', 'placeholder': 'الاسم العلمي'}),
            'originCountry': forms.TextInput(
                attrs={'class': 'form-control col-md-3', 'placeholder': 'بلد التصنيع'}),
            'arabicName': forms.TextInput(
                attrs={'class': 'form-control col-md-3', 'placeholder': 'الاسم باللغة العربية'}),
            'manufactureCompanyAr': forms.TextInput(
                attrs={'class': 'form-control col-md-3', 'placeholder': 'الشركة المصنعة باللغة العربية'}),
            'manufactureCompanyEn': forms.TextInput(
                attrs={'class': 'form-control col-md-3', 'placeholder': 'الشركة المصنعة باللغة الإنجليزية'}),
            'category': forms.Select(attrs={'class': 'form-control col-md-3', 'style': 'margin:0 0 10px;'}),
            'type': forms.Select(attrs={'class': 'form-control col-md-3', 'style': 'margin:0 0 10px;'}),
        }


class medicineEditForm(forms.ModelForm):

    class Meta:
        model = medicine
        fields = '__all__'
        exclude = ['generalName', 'scientificName', 'originCountry', 'manufactureCompanyEn']
        labels = {
            'generalName': 'الإسم التجاري بالإنجليزي',
            'arabicName': 'الإسم التجاري بالعربي',
            'scientificName': 'الإسم العلمي',
            'manufactureCompanyAr': 'الشركة المصنعة باللغة العربية',
            'manufactureCompanyEn': 'الشركة المصنعة باللغة الإنجليزية',
            'img': 'صورة الدواء :',
            'type': 'نوع الدواء :',
            'originCountry': 'بلد التصنيع',
            'category': 'تصنيف الدواء :',
        }
        widgets = {
            'generalName': forms.TextInput(attrs={'class': 'form-control col-md-3', 'placeholder': 'الاسم التجاري باللغة الإنجليزية', 'disabled': 'True'}),
            'scientificName': forms.TextInput(
                attrs={'class': 'form-control col-md-3 mb-3', 'placeholder': 'الاسم العلمي', 'disabled': 'True'}),
            'arabicName': forms.TextInput(
                attrs={'class': 'form-control col-md-3', 'placeholder': 'الاسم باللغة العربية'}),
            'originCountry': forms.TextInput(
                attrs={'class': 'form-control col-md-3', 'placeholder': 'بلد التصنيع', 'disabled': 'True'}),
            'manufactureCompanyAr': forms.TextInput(
                attrs={'class': 'form-control col-md-3', 'placeholder': 'الشركة المصنعة باللغة العربية'}),
            'manufactureCompanyEn': forms.TextInput(
                attrs={'class': 'form-control col-md-3', 'placeholder': 'الشركة المصنعة باللغة الإنجليزية', 'disabled': 'True'}),
            'category': forms.Select(attrs={'class': 'form-control col-md-3', 'style': 'margin:0 0 10px;'}),
            'type': forms.Select(attrs={'class': 'form-control col-md-3', 'style': 'margin:0 0 10px;'}),
        }


class locationForm(forms.ModelForm):
    class Meta:
        model = location
        fields = ['city', 'location', 'locUrl']
        exelude = ['username']

        labels = {
            'location': '',
            'city': '',
            'locUrl': '',
        }

        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control col-md-12 mb-3', 'placeholder': 'الموقع'}),
            'city': forms.TextInput(attrs={'class': 'form-control col-md-12', 'placeholder': 'المدينة'}),
            'locUrl': forms.URLInput(attrs={'class': 'form-control col-md-12', 'placeholder': 'رابط الموقع من برنامج خرائط جوجل'}),
        }


class addToStorageForm(forms.ModelForm):
    class Meta:
        model = storage
        fields = '__all__'
        exclude = ['username', 'is_Available']

        labels = {
            'price': '',
            'medicine': '',
        }
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-control col-md-12 col-12 mb-3', 'placeholder': 'الدواء'}),
            'price': forms.TextInput(attrs={'class': 'form-control col-md-3 mb-3', 'placeholder': 'السعر(إختياري)'}),
        }


class editStorageForm(forms.ModelForm):
    medicine = forms.ModelChoiceField(queryset=medicine.objects.all(), disabled=True, label='', required=False)

    class Meta:
        model = storage
        fields = ['medicine', 'price', 'is_Available']
        exclude = ['username', 'dose']

        labels = {
            'price': '',
            'is_Available': 'متوفر  ',
            'medicine': '',
        }

        widgets = {
            'price': forms.TextInput(attrs={'class': 'form-control col-md-3 mb-3', 'placeholder': 'السعر'}),
        }


class userInfoForm(forms.ModelForm):
    class Meta:
        model = user_info
        fields = ['accType']
        exclude = ['username']
        labels = {
            'accType': 'نوع الحساب',
        }

        widgets = {
            'accType': forms.RadioSelect(
                attrs={'class': 'col-md-12', 'onclick': 'javascript:AccTypeCheck()'}),
        }



class PharmacyAccForm(forms.ModelForm):
    class Meta:
        model = pharmacyAcc
        fields = ['pharmacyName', 'phone_number',
                  'whatsappNumber', 'facebookPage', 'licenseNumber', 'licenseImg']
        exclude = ['username']
        labels = {
            'pharmacyName': '',
            'phone_number': '',
            'facebookPage': '',
            'whatsappNumber': '',
            'licenseImg': 'صورة من ترخيص الصيدلية',
            'licenseNumber': '',
        }

        widgets = {
            'pharmacyName': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': 'إسم الصيدلية',}),
            'licenseNumber': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': 'رقم الترخيص',}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'رقم الجوال (249xxxxxxxxx)'}),
            'facebookPage': forms.URLInput(attrs={'class': 'form-control',
                                                  'placeholder': 'رابط صفحة الفيسبوك',}),
            'whatsappNumber': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'رقم الواتس أب (249xxxxxxxxx)'}),
        }

class CustomerAccForm(forms.ModelForm):
    class Meta:
        model = CustomerAcc
        fields = ['phone_number']
        exclude = ['username']
        labels = {
            'phone_number': '',
        }

        widgets = {
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'رقم الجوال (249xxxxxxxxx)'}),
        }


class organizationAccForm(forms.ModelForm):
    class Meta:
        model = organizationAcc
        fields = ['organizationName', 'phone_number', 'whatsappNumber', 'facebookPage']
        exclude = ['username']
        labels = {
            'organizationName': '',
            'phone_number': '',
            'facebookPage': '',
            'whatsappNumber': '',
        }

        widgets = {
            'organizationName': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': 'إسم المبادرة',}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'رقم الجوال (249xxxxxxxxx)'}),
            'facebookPage': forms.URLInput(attrs={'class': 'form-control',
                                                  'placeholder': 'رابط صفحة الفيسبوك',}),
            'whatsappNumber': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'رقم الواتس أب (249xxxxxxxxx)'}),
        }


class PharmacyAccEditForm(forms.ModelForm):
    class Meta:
        model = pharmacyAcc
        fields = ['whatsappNumber', 'facebookPage', 'phone_number']
        exclude = ['username', 'pharmacyName', 'licenseNumber', 'licenseImg']
        labels = {
            'phone_number': '',
            'facebookPage': '',
            'whatsappNumber': '',
        }

        widgets = {
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'رقم الجوال (249xxxxxxxxx)'}),
            'facebookPage': forms.URLInput(attrs={'class': 'form-control',
                                                  'placeholder': 'رابط صفحة الفيسبوك',}),
            'whatsappNumber': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'رقم الواتس أب (249xxxxxxxxx)'}),
        }

class organizationAccEditForm(forms.ModelForm):
    class Meta:
        model = organizationAcc
        fields = ['phone_number', 'whatsappNumber', 'facebookPage']
        exclude = ['username', 'organizationName']
        labels = {
            'phone_number': '',
            'facebookPage': '',
            'whatsappNumber': '',
        }

        widgets = {
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'رقم الجوال (249xxxxxxxxx)'}),
            'facebookPage': forms.URLInput(attrs={'class': 'form-control',
                                                  'placeholder': 'رابط صفحة الفيسبوك',}),
            'whatsappNumber': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'رقم الواتس أب (249xxxxxxxxx)'}),
        }



class loginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'إسم المستخدم أو البريد الإلكتروني'}),
        label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'كلمة السر'}),
                               label='')

    def clean_password(self):
        data = self.cleaned_data['password']
        if len(data) < 8:
            raise forms.ValidationError("أدخل كلمة سر صحيحة")
        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        if '@' in data:
            email = User.objects.get(email=data)
            return email
        else:
            return data


class registerForm(forms.Form):
    username2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'إسم المستخدم أو البريد الإلكتروني'}),
        label='')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الإسم الأول'}),
                                 label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الإسم الأخير'}),
                                label='')
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'كلمة السر'}),
                                label='')
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'أعد إدخال كلمة السر'}), label='')

    def clean_password1(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        if pass1 == pass2:
            return pass1
        else:
            raise forms.ValidationError("كلمة السر غير متطابقة")

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("الإيميل مستخدم")
        else:
            return email

    def clean_username2(self):
        data = self.cleaned_data['username2']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('الإسم مستخدم الرجاء تجربة إسم أخر')
        elif not User.objects.filter(username=data).exists():
            return data


class requestMedForm(forms.ModelForm):
    class Meta:
        model = requestMedi
        fields = ['type', 'medicineGeneral', 'description', 'prescription', 'img']
        exclude = ['username']

        labels = {
            'dose': '',
            'type': 'الرجاء تحديد النوع طلب / تبرع',
            'medicineGeneral': '',
            'description': '',
            'img': 'صورة للدواء',
            'prescription': 'الوصفة الطبية (الرورشتة)(الرجاء إضافتها في حالة الطلب)'
        }
        widgets = {
            'medicineGeneral': forms.TextInput(attrs={'class': 'form-control col-md-3', 'placeholder': 'إسم الدواء'}),
            'type': forms.Select(attrs={'class': 'form-control col-md-3 mt-0'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control col-md-6 mb-3', 'placeholder': 'الوصف (إختياري)', 'style': 'height: 100px;'}),
            'prescription': forms.FileInput(attrs={'class': 'col-md-12 mb-3 mt-0'}),
            'img': forms.FileInput(attrs={'class': 'col-md-12 mb-3'}, ),
        }


class contactForm(forms.Form):
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الموضوع'}),
                              label='')
    message = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'الرجاء كتابة معلومات التواصل في اخر الرسالة'}),
                              label='')


class addBranchForm(forms.ModelForm):
    class Meta:
        model = location
        fields = ['city', 'location', 'locUrl']
        exclude = ['username']

        labels = {
            'city': '',
            'location': '',
            'locUrl': '',
        }
        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control col-md-6 mb-3', 'placeholder': 'المدينة'}),
            'location': forms.TextInput(attrs={'class': 'form-control col-md-6', 'placeholder': 'الموقع'}),
            'locUrl': forms.URLInput(attrs={'class': 'form-control col-md-12', 'placeholder': 'رابط الموقع من برنامج خرائط جوجل'}),
        }