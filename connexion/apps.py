from django.apps import AppConfig


class ConnexionConfig(AppConfig):
    name = 'connexion'

    def ready(self):
    	import connexion.signals