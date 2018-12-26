from django.contrib import admin
from .models import NouvelleEcrite, Tag



class NouvelleEcriteAdmin(admin.ModelAdmin):
   list_display   = ('titre', 'auteur_nouvelle', 'date')
   list_filter    = ('tag',) 
   date_hierarchy = 'date'
   ordering       = ('date', )
   search_fields  = ('titre', 'contenu', 'auteur_nouvelle')
   prepopulated_fields = {'slug': ('titre', ), }

    # Configuration du formulaire d'édition
   fieldsets = (
        # Fieldset 1 : info auteur du billet 'classes': ['collapse', ],
       ('Auteur de l\'article ', {
       		
       		'fields': ('auteur_nouvelle', 'date', )
       	}),
       # Fieldset 2 : meta-info (titre, auteur…)
       ('Information livre', {
            
            'fields': ('titre', 'slug', 'tag', 'likes') 
        }),
        # Fieldset 2 : contenu de l'article
        ('Contenu de l\'article', {
           'description': 'Le formulaire accepte les balises HTML. Utilisez-les à bon escient !',
           'fields': ( 'contenu', 'information_additionnelle')
        }),
    )
admin.site.register(NouvelleEcrite, NouvelleEcriteAdmin)
admin.site.register(Tag)
