from rest_framework import serializers
from .models import FitnessClass, Booking

class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'instructor', 'date_time', 'available_slots']

class BookingRequestSerializer(serializers.Serializer):
    # This serializer is for the incoming booking request payload
    class_id = serializers.IntegerField()
    client_name = serializers.CharField(max_length=100)
    client_email = serializers.EmailField()

class BookingSerializer(serializers.ModelSerializer):
    # This serializer is for returning booking details
    fitness_class = FitnessClassSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'client_name', 'client_email', 'fitness_class']