from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Order

class Command(BaseCommand):
    help = 'Delete cancelled orders that are older than 24 hours'

    def handle(self, *args, **options):
        # Calculate cutoff time: 24 hours ago
        cutoff_time = timezone.now() - timedelta(hours=24)
        
        # Find cancelled orders older than 24 hours
        old_cancelled_orders = Order.objects.filter(
            status='CANCELLED',
            cancelled_at__lt=cutoff_time
        )
        
        count = old_cancelled_orders.count()
        
        if count > 0:
            old_cancelled_orders.delete()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {count} cancelled orders older than 24 hours')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('No cancelled orders older than 24 hours found')
            )