from django.apps import AppConfig


class BlogLivresfConfig(AppConfig):
    name = 'blog_livreSF'
    
    def ready(self):
    	import blog_livreSF.signals