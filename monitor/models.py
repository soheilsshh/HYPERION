from django.db import models

class Service(models.Model):
    TYPE_CHOICES = [('http', 'HTTP'), ('container', 'Docker')]
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255)  
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    interval = models.IntegerField(default=5)  
    is_active = models.BooleanField(default=True)

class UserAlert(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    email = models.EmailField()