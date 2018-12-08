from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):

    # Configuration du formulaire d'édition
   fieldsets = (
        # Fieldset 1 : info auteur du billet'classes': ['collapse', ],
       ('Profile_perso ', {
       		
       		'fields': ('nom', 'prenom', 'birth_date',  )
       	}),
       # Fieldset 2 : meta-info (titre, auteur…)
       ('Profile_virtuel', {
            
            'fields': ( 'avatar','pseudo', 'slug_pseudo', 'signature', 'nombre_post_ecrit', 'rang') #, 'categorie')
        }),

    )
# admin.site.register(Categorie)
admin.site.register(Profile, ProfileAdmin)