from django.urls import path
from purchase_order.api.views import PurchaseOrderListCreateAPIView, PurchaseOrderRetrieveUpdateDestroyAPIView,AcknowledgePurchaseOrder

urlpatterns = [
    path('api/purchase_orders/', PurchaseOrderListCreateAPIView.as_view(), name='purchase-order-list-create'),
    path('api/purchase_orders/<int:po_id>/', PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(), name='purchase-order-retrieve-update-destroy'),
    path('api/purchase_orders/<int:po_id>/acknowledge/',AcknowledgePurchaseOrder.as_view(),name="AcknowledgementDetail"),

]