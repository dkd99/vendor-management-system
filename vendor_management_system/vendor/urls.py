from django.urls import path
from vendor.api.views import VendorListCreateAPIView, VendorRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('api/vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('api/vendors/<int:vendor_id>/', VendorRetrieveUpdateDestroyAPIView.as_view(), name='vendor-retrieve-update-destroy'),
]