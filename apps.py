from django.apps import AppConfig


class RechargeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vtu_app'
# vtu/apps.py

def ready(self):
    import vtu_project.signals
    # Ensure signals are registered when the app is ready
    super().ready()