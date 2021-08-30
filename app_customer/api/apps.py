import logging
import os

from django.apps import AppConfig


class ApiConfig(AppConfig):

    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        logging.info(f"Aplicação iniciada pid={os.getpid()}...")
