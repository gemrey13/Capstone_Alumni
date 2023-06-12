from django.apps import AppConfig


class AlumnimanagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AlumniManagement'

    def ready(self):
        import AlumniManagement.signals  # Import the signals module

    
