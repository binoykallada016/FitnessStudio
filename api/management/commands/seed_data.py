from django.core.management.base import BaseCommand
from api.models import FitnessClass, Booking
from datetime import datetime, timedelta
import pytz

class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Booking.objects.all().delete()
        FitnessClass.objects.all().delete()

        self.stdout.write("Seeding data...")

        # Get the IST timezone
        ist = pytz.timezone('Asia/Kolkata')

        # Create sample classes
        FitnessClass.objects.create(
            name = "Yoga Flow",
            instructor = "Angel John",
            date_time = ist.localize(datetime.now() + timedelta(days = 2, hours = 3)),
            available_slots = 20                                                 
        )
        FitnessClass.objects.create(
            name = "Zumba Party",
            instructor = "Bithul Krishna",
            date_time = ist.localize(datetime.now() + timedelta(days = 3, hours = 5)),
            available_slots = 15
        )
        FitnessClass.objects.create(
            name = "HIIT Blast",
            instructor = "Aleena Jose",
            date_time = ist.localize(datetime.now() + timedelta(days = 4, hours = 1)),
            available_slots = 1
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded data!'))
