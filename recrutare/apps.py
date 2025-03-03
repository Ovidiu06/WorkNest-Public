from django.apps import AppConfig


class RecrutareConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recrutare'

    def ready(self):
        print('Incarcare aplicatie Recrutare')
        from . import signals