from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsVendorOrReadOnly(BasePermission):
    """
    Custom permission to only allow vendors assigned to the purchase order to edit it.
    """
    def has_permission(self, request, view): 
        if request.method in ['POST']:
            return False
        elif request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ['PUT','DELETE','PATCH']:
            return True 
        elif request.method in ['DELETE'] and request.user.is_staff:
            return True
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, or OPTIONS requests4

        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ['PUT', 'PATCH']:
            if obj.on_time_delivery_rate != request.data.get("on_time_delivery_rate") or \
               obj.quality_rating_avg != request.data.get("quality_rating_avg") or \
               obj.average_response_time != request.data.get("average_response_time") or \
               obj.fulfillment_rate != request.data.get("fulfillment_rate") or \
               obj.vendor_code != request.data.get("vendor_code"):
                return False  # Prevent vendors from updating the four specified fields
        print((obj.vendor_code == str(request.user)),">>>>>>>>>>>>>>>>")
        # Check if the user making the request is a vendor assigned to the purchase order
        return (obj.vendor_code == str(request.user)) or request.user.is_staff