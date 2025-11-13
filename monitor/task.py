# monitoring/tasks.py
import requests
import subprocess
from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from .models import Service

@shared_task
def check_all_services():
    now = timezone.now()
    services = Service.objects.filter(is_active=True)

    for service in services:
        time_since_last_check = now - service.last_checked
        if time_since_last_check >= timedelta(minutes=service.interval):
            _check_single_service(service)

def _check_single_service(service):
 
    try:
        if service.type == 'http':
            response = requests.get(service.url, timeout=10)
            service.status = (response.status_code == 200)
        elif service.type == 'container':
            
            host = service.url.replace('http://', '').replace('https://', '').split('/')[0]
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '3', host],
                capture_output=True
            )
            service.status = (result.returncode == 0)
        else:
            service.status = False  
    except Exception:
        service.status = False

    service.save(update_fields=['status', 'last_checked'])