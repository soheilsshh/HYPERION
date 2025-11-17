
from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=500, unique=True)
    
    db_username = models.CharField(max_length=100, blank=True, null=True)
    db_password = models.CharField(max_length=200, blank=True, null=True)
    db_database = models.CharField(max_length=200, blank=True, null=True)

    interval = models.PositiveIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    last_checked = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.url})"

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Service"
        indexes = [models.Index(fields=['url']), models.Index(fields=['is_active'])]


class UserAlert(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='alerts')
    email = models.EmailField()

    def __str__(self):
        return f"Alert for {self.service.name} → {self.email}"

    class Meta:
        unique_together = ('service', 'email')  