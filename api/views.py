# from django.shortcuts import render

# # Create your views here.

# api/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from django.db import transaction
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer, BookingRequestSerializer

class ClassListView(generics.ListAPIView):
    """
    GET /classes
    Returns a list of all upcoming fitness classes.
    """
    queryset = FitnessClass.objects.filter(available_slots__gt=0).order_by('date_time')
    serializer_class = FitnessClassSerializer

class BookClassView(generics.GenericAPIView):
    """
    POST /book
    Accepts a booking request and creates a booking if slots are available.
    """
    serializer_class = BookingRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) # Validates input fields

        class_id = serializer.validated_data['class_id']
        client_name = serializer.validated_data['client_name']
        client_email = serializer.validated_data['client_email']

        try:
            # Use a transaction to ensure data integrity
            with transaction.atomic():
                # Lock the class row to prevent race conditions (overbooking)
                fitness_class = FitnessClass.objects.select_for_update().get(id=class_id)

                if fitness_class.available_slots <= 0:
                    return Response({"error": "No available slots for this class."}, status=status.HTTP_400_BAD_REQUEST)

                # Reduce slots and save
                fitness_class.available_slots -= 1
                fitness_class.save()

                # Create the booking
                booking = Booking.objects.create(
                    client_name=client_name,
                    client_email=client_email,
                    fitness_class=fitness_class
                )

                return Response(
                    {"success": "Booking successful!", "booking_id": booking.id},
                    status=status.HTTP_201_CREATED
                )
        except FitnessClass.DoesNotExist:
            return Response({"error": "Class not found."}, status=status.HTTP_404_NOT_FOUND)

class UserBookingsListView(generics.ListAPIView):
    """
    GET /bookings?email=<email>
    Returns all bookings made by a specific email address.
    """
    serializer_class = BookingSerializer

    def get_queryset(self):
        email = self.request.query_params.get('email', None)
        if email:
            return Booking.objects.filter(client_email=email)
        return Booking.objects.none() # Return nothing if no email is provided