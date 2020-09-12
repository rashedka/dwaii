from django.db import models
from django.contrib.auth.models import User
import uuid
import os

# Create your models here.

# comment

accountType = [
    ('no', 'عادي'),
    ('ph', 'صيدلية'),
    ('or', 'مبادرة'),
]

requestType = [
    ('request', 'طلب'),
    ('donate', 'تبرع'),
]


def encodePath(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('license/', filename)


class user_info(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    accType = models.CharField(default='no', choices=accountType, max_length=3)

    def __str__(self):
        return self.username.username


class pharmacyAcc(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    pharmacyName = models.CharField(max_length=100)
    facebookPage = models.URLField(max_length=200, null=True, blank=True)
    phone_number = models.BigIntegerField()
    whatsappNumber = models.BigIntegerField(null=True, blank=True)
    licenseImg = models.ImageField(upload_to=encodePath)
    licenseNumber = models.CharField(max_length=30)


class CustomerAcc(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.BigIntegerField()


class organizationAcc(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    organizationName = models.CharField(max_length=100)
    facebookPage = models.URLField(max_length=200, null=True, blank=True)
    phone_number = models.BigIntegerField()
    whatsappNumber = models.BigIntegerField(null=True, blank=True)



class medType(models.Model):
    typeEN = models.CharField(max_length=50)
    typeAR = models.CharField(max_length=50)

    def __str__(self):
        return self.typeAR


class medCategory(models.Model):
    categoryEN = models.CharField(max_length=50)
    categoryAR = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryAR


class medicine(models.Model):
    generalName = models.CharField(max_length=100)
    arabicName = models.CharField(max_length=100, null=True, blank=True)
    scientificName = models.CharField(max_length=100)
    originCountry = models.CharField(max_length=100)
    type = models.ForeignKey(medType, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(medCategory, on_delete=models.CASCADE, null=True, blank=True)
    manufactureCompanyAr = models.CharField(max_length=50, null=True, blank=True)
    manufactureCompanyEn = models.CharField(max_length=50)
    img = models.ImageField(upload_to="medicine/", default="profile.png")

    def __str__(self):
        return self.generalName


class storage(models.Model):
    medicine = models.ForeignKey(medicine, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField(null=True, blank=True)
    is_Available = models.BooleanField(default=True)
    updateDate = models.DateTimeField(auto_now=True)
    createDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "med : {} , pharmacy: {}".format(self.medicine.generalName, self.username)


class requestMedi(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    medicineGeneral = models.CharField(max_length=100)
    img = models.ImageField(upload_to="medicine/request/new/", default="profile.png", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    requestDate = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=requestType)
    prescription = models.ImageField(upload_to="medicine/request/", null=True, blank=True)

    def __str__(self):
        return "med : {} , user: {}".format(self.medicineGeneral, self.username)


class location(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    locUrl = models.URLField(max_length=200)
