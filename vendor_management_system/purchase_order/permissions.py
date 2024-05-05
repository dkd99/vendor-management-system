from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsVendorOrReadOnly(BasePermission):
    """
    Custom permission to only allow vendors assigned to the purchase order to edit it.
    """
    def has_permission(self, request, view): 
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        if request.method in ['PUT','DELETE','PATCH']:
            return True  # Always allow PUT requests
        return  request.user.is_staff      
    def has_object_permission(self, request, view, obj):

        # Allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user making the request is a vendor assigned to the purchase order
        if isinstance(obj.vendor,str):    
  
            return (obj.vendor == str(request.user)) or request.user.is_staff
            
        return (obj.vendor.vendor_code == str(request.user)) or request.user.is_staff
