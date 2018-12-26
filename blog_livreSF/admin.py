from django.contrib import admin
from .models import Article, Genre



class ArticleAdmin(admin.ModelAdmin):
   list_display   = ('titre', 'auteur_blog', 'date')
   list_filter    = ('auteur_livre',) 
   date_hierarchy = 'date'
   ordering       = ('date', )
   search_fields  = ('titre', 'contenu', 'auteur_blog')
   prepopulated_fields = {'slug': ('titre', ), }

    # Configuration du formulaire d'édition
   fieldsets = (
        # Fieldset 1 : info auteur du billet 'classes': ['collapse', ],
       ('Auteur de l\'article ', {
       		
       		'fields': ('auteur_blog', 'date', )
       	}),
       # Fieldset 2 : meta-info (titre, auteur…)
       ('Information livre', {
            
            'fields': ('titre', 'slug', 'auteur_livre', 'genre', 'likes') 
        }),
        # Fieldset 2 : contenu de l'article
        ('Contenu de l\'article', {
           'description': 'Le formulaire accepte les balises HTML. Utilisez-les à bon escient !',
           'fields': ('resume', 'source_resume', 'contenu', 'source_contenu', 'photo')
        }),
    )
# admin.site.register(Categorie)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Genre)
