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
