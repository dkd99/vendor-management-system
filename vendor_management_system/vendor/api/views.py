from vendor.models import Vendor
from rest_framework.views import APIView
from .serializers import VendorSerializer
from rest_framework.response import Response
from rest_framework import generics
from vendor.permissions import IsVendorOrReadOnly

class VendorListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsVendorOrReadOnly]

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsVendorOrReadOnly]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_url_kwarg = 'vendor_id'