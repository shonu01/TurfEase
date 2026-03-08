from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:turf_id>/', views.book_turf, name='book_turf'),
    path('confirm/', views.confirm_booking, name='confirm_booking'),
    path('cancel/<int:pk>/', views.cancel_booking, name='cancel_booking'),
    path('receipt/<int:pk>/', views.booking_receipt, name='booking_receipt'),
    path('cancelled-receipt/<int:pk>/', views.cancelled_receipt, name='cancelled_receipt'),
    path('history/', views.booking_history, name='booking_history'),
    path('notifications/', views.notifications_view, name='notifications'),
]
