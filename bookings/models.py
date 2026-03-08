from django.db import models
from django.contrib.auth.models import User
from turfs.models import Turf


class Booking(models.Model):
    MEMBER_CHOICES = [
        (5, '5-a-side'),
        (7, '7-a-side'),
        (11, '11-a-side'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    members = models.PositiveIntegerField(choices=MEMBER_CHOICES, default=5)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.turf.name} on {self.booking_date}"

    class Meta:
        ordering = ['-created_at']


class CancelledBooking(models.Model):
    """Records bookings cancelled due to admin maintenance blocks — serves as refund receipt."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cancelled_bookings')
    turf = models.ForeignKey(Turf, on_delete=models.SET_NULL, null=True, related_name='cancelled_bookings')
    turf_name = models.CharField(max_length=200)
    turf_location = models.CharField(max_length=300)
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    members = models.PositiveIntegerField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=500, default='Cancelled due to maintenance')
    cancelled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cancelled: {self.user.username} - {self.turf_name} on {self.booking_date}"

    class Meta:
        ordering = ['-cancelled_at']


class Notification(models.Model):
    """In-app notifications for users (e.g. maintenance cancellations)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=300, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.title}"

    class Meta:
        ordering = ['-created_at']
