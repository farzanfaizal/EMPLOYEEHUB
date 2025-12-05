from django.apps import AppConfig


class EmpAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emp_app'
    verbose_name = 'Employee Management'

    def ready(self):
        """Import signals when app is ready"""
        import emp_app.signals  # noqa
