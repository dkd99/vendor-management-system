from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from vendor.models import Vendor 
from historical_performance.models import HistoricalPerformance

@receiver(pre_save, sender=Vendor)
def update_historical_performance(sender, instance, **kwargs):
    # Check if the vendor already exists
    if instance.pk:
        # Get the last historical performance record for this vendor
        last_record = HistoricalPerformance.objects.filter(vendor=instance).latest('date')
        # Check if a week has passed since the last update
        if timezone.now() - last_record.date >= timezone.timedelta(weeks=1):
            # Update the historical performance model with the new metrics
            HistoricalPerformance.objects.create(
                vendor=instance.id,
                date=timezone.now(),
                on_time_delivery_rate=instance.on_time_delivery_rate,
                quality_rating_avg=instance.quality_rating_avg,
                average_response_time=instance.average_response_time,
                fulfillment_rate=instance.fulfillment_rate
            )
