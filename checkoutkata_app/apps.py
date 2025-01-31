from django.apps import AppConfig


class CheckoutkataAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkoutkata_app'

    def ready(self):
        import checkoutkata_app.signals

        
