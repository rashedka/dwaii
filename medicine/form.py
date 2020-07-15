from django import forms

from .models import medicine, storage, user_info


class medicineForm(forms.ModelForm):
    class Meta:
        model = medicine
        fields = '__all__'
        labels = {
            'generalName': '',
            'scientificName': '',
            'img': 'صورة الدواء'
        }
        widgets = {
            'generalName': forms.TextInput(attrs={'class': 'form-control col-md-3', 'placeholder': 'الاسم التجاري'}),
            'scientificName': forms.TextInput(attrs={'class': 'form-control col-md-3 mb-3', 'placeholder': 'الاسم العلمي'})
        }


class addToStorageForm(forms.ModelForm):
    class Meta:
        model = storage
        fields = '__all__'
        exclude = ['username', 'is_Available']

        labels = {
            'price': '',
            'dose': '',
            'medicine': 'إٍسم الدواء التجاري',
        }
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-control col-md-3'}),
            'price': forms.TextInput(attrs={'class': 'form-control col-md-3 mb-3', 'placeholder': 'السعر'}),
            'dose': forms.TextInput(attrs={'class': 'form-control col-md-3', 'placeholder': 'الجرعة'}),

        }


class userInfoForm(forms.ModelForm):
    class Meta:
        model = user_info
        fields = ['pharmacyName', 'city', 'location', 'phone_number',
                  'whatsappNumber', 'facebookPage', 'is_pharmacy']
        exclude = ['username', 'is_pharmacy']
        labels = {
            'pharmacyName': '',
            'location': '',
            'phone_number': '',
            'city': '',
            'is_pharmacy': 'فضلا إذا كان الحساب خاص بصيدلية ضع علامة صح ',
            'facebookPage': '',
            'whatsappNumber': '',
        }

        widgets = {
            'pharmacyName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أسم الصيدلية'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الموقع'}),
            'is_pharmacy': forms.CheckboxInput(attrs={'class': 'checkbox', 'style': 'margin-top :10px'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'رقم الجوال'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'المدينة'}),
            'facebookPage': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'رابط صفحة الفيسبوك'}),
            'whatsappNumber': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المدينة'}),

        }

