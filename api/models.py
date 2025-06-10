from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    available_slots = models.IntegerField(validators = [MinValueValidator(0)])

    def __str__(self):
        return f"{self.name} with {self.instructor} on {self.date_time.strftime('%Y-%m-%d %H:%M')}"

class Booking(models.Model):
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    fitness_class = models.ForeignKey(FitnessClass, on_delete = models.CASCADE, related_name = 'bookings')

    def __str__(self):
        return f"Booking for {self.client_name} in {self.fitness_class.name}"


