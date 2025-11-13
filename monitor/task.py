# monitor/tasks.py
import redis
from urllib.parse import urlparse
from django.utils import timezone
from celery import shared_task
from .models import Service

@shared_task
def check_redis_services():
    services = Service.objects.filter(
        is_active=True,
        url__startswith='redis://'
    )

    for service in services:
        time_since_last = timezone.now() - service.last_checked
        if time_since_last < timezone.timedelta(minutes=service.interval):
            continue  


        parsed = urlparse(service.url)
        host = parsed.hostname
        port = parsed.port or 6379
        db = int(parsed.path.lstrip('/')) if parsed.path and parsed.path != '/' else 0

        try:
            r = redis.Redis(host=host, port=port, db=db, socket_connect_timeout=3)
            r.ping() 
            service.status = True
            print(f"Redis UP: {service.name} ({service.url})")

        except Exception as e:
            service.status = False
            
            print(f"\033[91mWARNING: Redis DOWN: {service.name} ({service.url}) | دلیل: {e}\033[0m")

        service.save(update_fields=['status', 'last_checked'])