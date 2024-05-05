from django.db import models
from vendor.models import Vendor

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,to_field="vendor_code")
    order_date = models.DateTimeField(auto_now_add=True, blank = False)
    delivery_date = models.DateTimeField(blank = False)
    items = models.JSONField(blank = False)
    quantity = models.PositiveIntegerField(blank = False)
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.po_number
