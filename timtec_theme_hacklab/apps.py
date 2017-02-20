from django.apps import AppConfig


class TimtecThemeHacklabConfig(AppConfig):
    name = 'timtec_theme_hacklab'
    verbose_name = 'Timtec Theme Hacklab'

    def ready(self):
        import timtec_theme_hacklab.signals
