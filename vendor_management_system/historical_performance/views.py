from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import HistoricalPerformance
from .serializers import HistoricalPerformanceSerializer

class VendorPerformanceAPIView(generics.ListAPIView):
    serializer_class = HistoricalPerformanceSerializer

    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        return HistoricalPerformance.objects.filter(vendor_id=vendor_id)