from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile

# Dans views.py

# user = form.save() #Première étape, sauvegarder utilisateur 

# userprofile = Profile.objects.get(user=user) #On va le chercher parce que grâce à signal.py on l'avait crée
# Ensuite on peut sauvegarder les champs que l'on veut userprofile.pseudo = profile_form.cleaned_data['pseudo']

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
# 	if created:
# 		Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()