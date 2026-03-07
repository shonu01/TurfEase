from django.db import models


class Turf(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    description = models.TextField()
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    price_5a_side = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Additional fixed price for 5-a-side teams')
    price_7a_side = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Additional fixed price for 7-a-side teams')
    image = models.ImageField(upload_to='turf_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MaintenanceBlock(models.Model):
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE, related_name='maintenance_blocks')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    reason = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.turf.name} - {self.date} ({self.start_time}-{self.end_time})"

    class Meta:
        ordering = ['-date', '-start_time']
