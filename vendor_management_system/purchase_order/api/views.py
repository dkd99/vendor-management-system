from rest_framework import generics
from purchase_order.models import PurchaseOrder
from purchase_order.api.serializers import PurchaseOrderSerializer
from purchase_order.permissions import IsVendorOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    #permission_classes = [IsVendorOrReadOnly]

    serializer_class = PurchaseOrderSerializer
    
    def get_queryset(self):
        queryset = PurchaseOrder.objects.all()
        vendor_code = self.request.query_params.get('vendor_code')
        if vendor_code:
            queryset = queryset.filter(vendor__vendor_code=vendor_code)
        return queryset

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsVendorOrReadOnly]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_url_kwarg = 'po_id'
    
class AcknowledgePurchaseOrder(APIView):
    permission_classes = [IsVendorOrReadOnly]
    
    def patch(self, request, id):
        try:
            po = PurchaseOrder.objects.get(id=id)
        except PurchaseOrder.DoesNotExist:
            return Response("Purchase order not found", status=status.HTTP_404_NOT_FOUND)
        
        acknowledgment_date = request.data.get('acknowledgment_date')
        
        if acknowledgment_date is not None:
            po.acknowledgment_date = acknowledgment_date
            po.save()
            serializer = PurchaseOrderSerializer(po)
            return Response(serializer.data)
        else:
            return Response("Please provide acknowledgment date", status=status.HTTP_400_BAD_REQUEST)