from django.db import models
from django.utils import timezone

class Target(models.Model):
    class CheckType(models.TextChoices):
        HTTP = "http", "HTTP request"
        TCP = "tcp", "TCP port check"

    class Status(models.TextChoices):
        UNKNOWN = "unknown", "Unknown"
        UP = "up", "Up"
        DOWN = "down", "Down"

    name = models.CharField(max_length=200)
    url = models.CharField(
        max_length=1000,
        help_text="Full URL (http://ip:port/ping) or host:port for TCP"
    )
    check_type = models.CharField(
        max_length=10,
        choices=CheckType.choices,
        default=CheckType.HTTP
    )

    interval_seconds = models.PositiveIntegerField(
        default=60,
        help_text="How often to check status (seconds)"
    )

    timeout_seconds = models.FloatField(default=3.0)

    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UNKNOWN
    )
    last_check_at = models.DateTimeField(null=True, blank=True)
    last_response_ms = models.FloatField(null=True, blank=True)
    failure_count = models.PositiveIntegerField(default=0)

    def mark_up(self, response_ms):
        self.status = self.Status.UP
        self.failure_count = 0
        self.last_response_ms = response_ms
        self.last_check_at = timezone.now()
        self.save()

    def mark_down(self):
        self.status = self.Status.DOWN
        self.failure_count += 1
        self.last_check_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.name} ({self.status})"
    

class AlertRule(models.Model):
    target = models.ForeignKey(Target, on_delete=models.CASCADE, related_name="alerts")
    enabled = models.BooleanField(default=True)
    
    failure_threshold = models.PositiveIntegerField(
        default=3,
        help_text="Trigger alert after N consecutive failures"
    )
    
    notify_email = models.EmailField(blank=True)
    notify_webhook = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return f"Alert for {self.target.name}"
