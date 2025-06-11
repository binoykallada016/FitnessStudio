# api/urls.py
from django.urls import path
from .views import ClassListView, BookClassView, UserBookingsListView

urlpatterns = [
    path('classes', ClassListView.as_view(), name='class-list'),
    path('book', BookClassView.as_view(), name='book-class'),
    path('bookings', UserBookingsListView.as_view(), name='user-bookings'),
]