from django.db import models

from plant_care_tracker.models.plant import Plant


class CareEvent(models.Model):
    EVENT_CHOICES = [
        ("water", "Watering"),
        ("fertilize", "Fertilizing"),
        ("repot", "Repotting"),
        ("disease", "Disease"),
        ("other", "Other"),
    ]
    plant = models.ForeignKey(
        Plant, on_delete=models.CASCADE, related_name="care_events"
    )
    event_type = models.CharField(max_length=10, choices=EVENT_CHOICES)
    date = models.DateField()
    notes = models.TextField(blank=True)
