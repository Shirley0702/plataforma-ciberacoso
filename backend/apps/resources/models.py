from django.db import models


class OrientationResource(models.Model):
    name = models.CharField(max_length=160)
    description = models.TextField()
    url = models.URLField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    country = models.CharField(max_length=80, default="Ecuador")
    emergency = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("-emergency", "order", "id")

    def __str__(self):
        return self.name
