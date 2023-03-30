from rest_framework.validators import UniqueTogetherValidator

from .models import *
from rest_framework import serializers


class Types(serializers.ModelSerializer):
    class Meta:
        model = medType
        fields = ['typeAR', 'typeEN']


class MedicineList(serializers.ModelSerializer):
    type = Types(many=False, read_only=True)

    class Meta:
        model = medicine
        fields = ('id', 'generalName', 'scientificName', 'img', 'type')


class Storagepharmacy(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    medicine = MedicineList(many=False, read_only=True)

    class Meta:
        model = storage
        fields = ('id', 'username', 'medicine')
        depth = 3

    def get_username(self, obj):
        Pharmacy = pharmacyAcc.objects.get(username=obj.username)
        return pharmacies(Pharmacy, many=False).data


class MedicinePharmacyList(serializers.ModelSerializer):
    Pharmacies = serializers.SerializerMethodField()
    isAvailable = serializers.SerializerMethodField()

    class Meta:
        model = medicine
        fields = ('generalName', 'Pharmacies', 'isAvailable')

    def get_Pharmacies(self, obj):
        pharmacyD = storage.objects.filter(medicine=obj)
        return Storagepharmacy(pharmacyD, many=True).data

    def get_isAvailable(self, obj):
        if storage.objects.filter(medicine=obj).exists:
            return 'sssss'
        else:
            return 'not available'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = location
        fields = ('id','location', 'city', 'locUrl')


class users(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class pharmacies(serializers.ModelSerializer):
    class Meta:
        model = pharmacyAcc
        fields = ('id','username', 'pharmacyName', 'licenseNumber', 'phone_number', 'whatsappNumber', 'facebookPage')


class StorageList(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    medicine = MedicineList(many=False, read_only=True)
    location = serializers.SerializerMethodField()

    class Meta:
        model = storage
        fields = ('id', 'username', 'medicine', 'location')
        depth = 3

    def get_username(self, obj):
        Pharmacy = pharmacyAcc.objects.get(username=obj.username)
        return pharmacies(Pharmacy, many=False).data

    def get_location(self, obj):
        Location = location.objects.filter(username=obj.username)
        return LocationSerializer(Location, many=True).data


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]
