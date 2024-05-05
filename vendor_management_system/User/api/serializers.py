from django.contrib.auth.models import User
from rest_framework import serializers
from vendor.models import Vendor

class VendorRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    name = serializers.CharField()
    contact_details = serializers.CharField()
    address = serializers.CharField()
    vendor_code = serializers.CharField()
    class Meta:
        model = User
        fields = ['name', 'contact_details','address' ,'vendor_code', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate(self, data):
        # Check if passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'error': 'Passwords do not match!'})



        # Check if vendor code is unique
        if Vendor.objects.filter(vendor_code=data['vendor_code']).exists():
            raise serializers.ValidationError({'error': 'Vendor code already exists!'})

        return data
    
    def save(self, **kwargs):
        vendor = Vendor(
            name=self.validated_data['name'],
            address=self.validated_data['address'],
            contact_details=self.validated_data['contact_details'],
            vendor_code=self.validated_data['vendor_code'],

        )
        password = self.validated_data['password']
        vendor.save()
        account = User(email=self.validated_data['contact_details'], username=self.validated_data['vendor_code'])
        account.set_password(password)
        account.save()
        return account
