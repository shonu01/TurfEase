from django.contrib import admin
from .models import Booking, CancelledBooking, Notification

admin.site.register(Booking)
admin.site.register(CancelledBooking)
admin.site.register(Notification)
