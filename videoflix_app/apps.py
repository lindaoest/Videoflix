from django.apps import AppConfig
from . import signals


class VideoflixAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videoflix_app'

    # def ready(self):
    #     import signals
