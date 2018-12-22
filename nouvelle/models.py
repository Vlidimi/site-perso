from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.urls import reverse


# Create your models here.


class Tag(models.Model):
	tags = models.CharField(max_length=30)

	def __str__(self):
		return self.tags

class NouvelleEcrite(models.Model):
	titre = models.CharField(max_length=100, help_text="Attention le titre ne doit pas excéder 100 caractères ")
	auteur_nouvelle = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.ManyToManyField(User, blank=True, related_name='nouvelle_likes')
	contenu = models.TextField(default='', help_text="Ecriture en markdown possible afin de structurer et d'accéder à des fonctionnalités d'HTML") #null=True
	date = models.DateTimeField(default=timezone.now, 
	          	              verbose_name="Date de parution")
	slug = models.SlugField(max_length=120)
	updated_at = models.DateTimeField(auto_now=True)
	modification = models.BooleanField(default=False)
	information_additionnelle = models.TextField(blank=True, default='', help_text="Ecriture en markdown possible afin de structurer et d'accéder à des fonctionnalités d'HTML")
	tag = models.ManyToManyField(Tag, blank=True, related_name='post_tag', help_text="N'hésitez pas à prendre un peu de temps pour spécifier quelques tags. C'est très pratique pour aiguiller le lecteur :) Si jamais le tag voulu n'apparait pas ici, vous pouvez en ajouter un en bas de ce formulaire ")

	def save(self, *args, **kwargs):
		self.slug = slugify(self.titre) #Permet de générer un slug à partir d'une chaine de caractères
		super(NouvelleEcrite, self).save(*args, **kwargs) 


	class Meta:
		verbose_name = "nouvelle"
		ordering = ['-date'] #Ordonne par rapport à la date

	def get_absolute_url(self):
		return reverse('nouvelle:show', kwargs={'id':self.id, 'slug':self.slug})

	def get_like_url(self):
		return reverse('nouvelle:like-toggle', kwargs={'id':self.id, 'slug':self.slug})

	def get_like_api_url(self):
		return reverse('nouvelle:like-api-toggle', kwargs={'id':self.id, 'slug':self.slug})

	def __str__(self):
		""" 
		Cette méthode que nous définirons dans tous les modèles
		nous permettra de reconnaître facilement les différents objets que 
		nous traiterons plus tard dans l'administration
		"""
		return "{0} de {1}".format(self.titre, self.auteur_nouvelle)