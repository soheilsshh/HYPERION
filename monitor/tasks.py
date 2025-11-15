import socket
import logging
import requests
from urllib.parse import urlparse
from django.utils import timezone
from celery import shared_task
from .models import Service

logger = logging.getLogger(__name__)

# Optional imports (they fail gracefully if not installed)
try: import redis
except: redis = None

try: import psycopg2
except: psycopg2 = None

try: import pymysql
except: pymysql = None

try: import pymongo
except: pymongo = None



def check_tcp(host, port, timeout=3):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except:
        return False


def check_http(url, timeout=4):
    try:
        r = requests.get(url, timeout=timeout)
        return r.status_code == 200
    except:
        return False



def check_redis(parsed, service):
    if not redis:
        logger.error("redis package not installed")
        return False

    try:
        conn = redis.Redis(
            host=parsed.hostname,
            port=parsed.port or 6379,
            db=int((parsed.path or "/0").replace("/", "")),
            username=service.username or parsed.username,
            password=service.password or parsed.password,
        )
        conn.ping()
        return True
    except Exception as e:
        logger.error(f"Redis error: {e}")
        return False


def check_postgres(parsed, service):
    if not psycopg2:
        logger.error("psycopg2 not installed")
        return False

    try:
        conn = psycopg2.connect(
            dbname=service.database or parsed.path.replace("/", ""),
            user=service.username or parsed.username,
            password=service.password or parsed.password,
            host=parsed.hostname,
            port=parsed.port or 5432,
            connect_timeout=3
        )
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Postgres error: {e}")
        return False


def check_mysql(parsed, service):
    if not pymysql:
        logger.error("pymysql not installed")
        return False

    try:
        conn = pymysql.connect(
            host=parsed.hostname,
            user=service.username or parsed.username,
            password=service.password or parsed.password,
            database=service.database or parsed.path.replace("/", ""),
            port=parsed.port or 3306,
            connect_timeout=3
        )
        conn.close()
        return True
    except Exception as e:
        logger.error(f"MySQL error: {e}")
        return False


def check_mongo(parsed, service):
    if not pymongo:
        logger.error("pymongo not installed")
        return False

    try:
        client = pymongo.MongoClient(
            host=parsed.hostname,
            port=parsed.port or 27017,
            username=service.username or parsed.username,
            password=service.password or parsed.password,
            serverSelectionTimeoutMS=3000
        )
        client.admin.command("ping")
        return True
    except Exception as e:
        logger.error(f"MongoDB error: {e}")
        return False



@shared_task
def check_single_service(service_id):
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return

    url = service.url.strip()
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()

    # Default: DOWN
    is_up = False

    # HTTP
    if scheme in ["http", "https"]:
        is_up = check_http(url)

    # Redis
    elif scheme == "redis":
        is_up = check_redis(parsed, service)

    # Postgres
    elif scheme in ["postgres", "postgresql"]:
        is_up = check_postgres(parsed, service)

    # MySQL
    elif scheme == "mysql":
        is_up = check_mysql(parsed, service)

    # MongoDB
    elif scheme == "mongodb":
        is_up = check_mongo(parsed, service)

    # RabbitMQ (AMQP)
    elif scheme in ["amqp", "amqps"]:
        is_up = check_tcp(parsed.hostname, parsed.port or 5672)

    # Kafka
    elif scheme == "kafka":
        is_up = check_tcp(parsed.hostname, parsed.port or 9092)

    # RAW TCP host:port
    elif ":" in url and scheme == "":
        try:
            host, port = url.split(":")
            is_up = check_tcp(host, int(port))
        except:
            is_up = False


    else:
        logger.error(f"Unsupported service type: {url}")
        is_up = False


    service.status = is_up
    service.last_checked = timezone.now()
    service.save(update_fields=["status", "last_checked"])

    msg = "UP" if is_up else "DOWN"
    logger.info(f"[{msg}] {service.name} → {service.url}")


@shared_task
def run_periodic_health_checks():
    now = timezone.now()

    services = Service.objects.filter(is_active=True)

    for service in services:

        if service.last_checked and (now - service.last_checked).seconds < service.interval:
            continue


        check_single_service.delay(service.id)
