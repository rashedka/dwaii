from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class user_info(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    pharmacyName = models.CharField(max_length=100, )
    city = models.CharField(max_length=50)
    phone_number = models.BigIntegerField()
    is_pharmacy = models.BooleanField(default=False)
    facebookPage = models.URLField(max_length=200)
    img = models.ImageField(upload_to="profile/", default="profile/profile.png", null=True, blank=True)

    def __str__(self):
        return self.username.username


class medicine(models.Model):
    generalName = models.CharField(max_length=100)
    scientificName = models.CharField(max_length=100, default='', blank=True)
    img = models.ImageField(upload_to="medicine/", default="profile.png", null=True, blank=True)

    def __str__(self):
        return self.generalName


class storage(models.Model):
    medicine = models.ForeignKey(medicine, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    is_Available = models.BooleanField(default=True)
    dose = models.CharField(max_length=50)
    updateDate = models.DateTimeField(auto_now=True)
    createDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "med : {} , pharmacy: {}".format(self.medicine.generalName, self.username)
