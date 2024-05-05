from django.urls import path
from .views import VendorPerformanceAPIView

urlpatterns = [
    path('api/vendors/<int:vendor_id>/performance/', VendorPerformanceAPIView.as_view(), name='vendor-performance'),
]