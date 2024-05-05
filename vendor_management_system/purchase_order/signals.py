from django.db.models.signals import  pre_save,post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Sum

@receiver(post_save, sender="purchase_order.PurchaseOrder")
def update_average_response_time(sender, instance, **kwargs):
    print("hereeeeeeeeeeeeeeeeee")
    if instance.acknowledgment_date:
        from .models import PurchaseOrder
        from vendor.models import Vendor
        vendor = instance.vendor
        print(vendor)
        previous_orders = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False).exclude(id=instance.id)
        total_response_time = instance.acknowledgment_date - instance.issue_date
        
        if previous_orders.exists():
            total_previous_response_time = sum([(po.acknowledgment_date - po.issue_date) for po in previous_orders], timezone.timedelta())
            total_response_time += total_previous_response_time
            total_orders = previous_orders.count() + 1
        else:
            total_orders = 1
        try:
            vendor_instance = Vendor.objects.get(vendor_code=vendor.vendor_code)
            average_response_time = total_response_time / total_orders
            vendor_instance.average_response_time = average_response_time.total_seconds() / 60  # Convert to minutes
            print(average_response_time.total_seconds() / 60,"=====================")
            vendor_instance.save()
        except Vendor.DoesNotExist:
            # Handle case where vendor does not exist
            pass

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

@receiver(pre_save, sender="purchase_order.PurchaseOrder")
def track_delivery_date(sender, instance, **kwargs):
    """
    Track delivery date changes before saving.
    """
    # Check if the status is being changed to completed
    print("track_delivery_date++++++++++++++++++++++++++++++++")
    from .models import PurchaseOrder

    if instance.status == 'completed':
        # Get the original instance before update
        try:
            original_instance = PurchaseOrder.objects.get(pk=instance.pk)
        except PurchaseOrder.DoesNotExist:
            return
        
        # Check if delivery date has changed

        instance.delivery_date_before_update = original_instance.delivery_date
        print(instance.delivery_date_before_update ,"=======================")


@receiver(post_save, sender="purchase_order.PurchaseOrder")
def update_on_time_delivery_rate(sender, instance, created, **kwargs):
    """
    Update on-time delivery rate when a purchase order is marked as completed.
    """
    # Check if the status is marked as completed and it's a new instance or delivery date has changed
    from .models import PurchaseOrder
    from vendor.models import Vendor

    print("update_on_time_delivery_rate++++++++++++++++++++++++++++++++")

    if instance.status == 'completed':
        vendor = instance.vendor
        total_completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
        print(total_completed_orders,"Total completed orders")
        
        print(instance.delivery_date_before_update >= instance.delivery_date,"instance.delivery_date_before_update >= instance.delivery_date")
        vendor_instance = Vendor.objects.get(vendor_code=vendor.vendor_code)

        orders_completed_before_expected = vendor_instance.on_time_delivery_rate*(total_completed_orders-1)
        print(vendor_instance.on_time_delivery_rate,total_completed_orders)
        print(total_completed_orders,orders_completed_before_expected,"===++++===")
        if instance.delivery_date_before_update >= instance.delivery_date:
            on_time_delivery_rate = (orders_completed_before_expected + 1) / (total_completed_orders)
        else:
            on_time_delivery_rate = (orders_completed_before_expected) / (total_completed_orders)
            
        # Get the total number of completed POs for that vendor

        # Calculate the on-time delivery rate

        # Update the vendor's on_time_delivery_rate
        vendor_instance.on_time_delivery_rate = on_time_delivery_rate
        vendor_instance.save()


@receiver(post_save, sender= "purchase_order.PurchaseOrder")
def update_quality_rating_average(sender, instance, created, **kwargs):
    """
    Update the quality rating average when a purchase order is marked as completed.
    """
    from .models import PurchaseOrder
    from vendor.models import Vendor
    
    if instance.quality_rating is not None and instance.status == 'completed':
        vendor = instance.vendor
        total_completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False).count()
        
        # Calculate the total quality rating for completed POs of the vendor
        total_quality_rating = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False).aggregate(total_rating=Sum('quality_rating'))['total_rating']
        
        # Calculate the average quality rating
        average_quality_rating = total_quality_rating / total_completed_orders
        
        # Update the vendor's quality_rating_average
        vendor_instance = Vendor.objects.get(vendor_code=vendor.vendor_code)

        vendor_instance.quality_rating_avg = average_quality_rating
        vendor_instance.save()
        
    @receiver(post_save, sender="purchase_order.PurchaseOrder")
    def update_fulfillment_rate(sender, instance, **kwargs):
        from .models import PurchaseOrder
        from vendor.models import Vendor
        vendor = instance.vendor
        # Get the total number of purchase orders for this vendor
        total_orders = PurchaseOrder.objects.filter(vendor=vendor,status__in=['completed', 'cancelled']).count()
        # Get the number of completed or cancelled purchase orders
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
        # Calculate the fulfillment rate
        fulfillment_rate = (completed_orders / total_orders) * 100 if total_orders > 0 else 0
        vendor_instance = Vendor.objects.get(vendor_code=vendor.vendor_code)
        vendor_instance.fulfillment_rate = fulfillment_rate
        vendor_instance.save()