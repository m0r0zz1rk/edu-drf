from apps.celery_app.celery_config import CeleryConfig

app = CeleryConfig().get_instance()
