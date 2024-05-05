from rest_framework import serializers
from purchase_order.models import PurchaseOrder

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        extra_kwargs = {
                    'quality_rating': {'allow_null': True},
                    'acknowledgment_date': {'allow_null': True},
                }