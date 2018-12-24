
from .forms import NouvelleForm, CommentSectionForm
from .models import NouvelleEcrite, Tag, CommentSection
from connexion.models import Profile
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt,csrf_protect 
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
	RedirectView,
)
def show(request, id, slug = ''):
	post = get_object_or_404(NouvelleEcrite, pk=id)
	nombre_mots = len(post.contenu.split())
	return render(request, 'nouvelle/show.html', {'nouvelleecrite': post, 'numero': id, 'nombre_mots':nombre_mots})

def show_blog(request, id, slug):
	post = get_object_or_404(NouvelleEcrite, pk=id)
	nombre_mots = len(post.contenu.split())
	if request.method == 'POST' and request.user.is_authenticated and 'laisser_commentaire' in request.POST:
	 	form = CommentSectionForm(request.POST)
	 	if form.is_valid():
	 		commentaire = form.save(commit=False)
	 		commentaire.auteur_comment = request.user
	 		commentaire.nouvelle = post
	 		commentaire.save()
	 		messages.success(request, "Commentaire envoyé ! Merci d'avoir pris le temps de partager votre avis :)")
	 		form = CommentSectionForm()
	 		return render(request, 'nouvelle/show.html', {'nouvelleecrite':post, 'form':form, 'nombre_mots':nombre_mots})

	elif request.method == 'POST' and request.user.is_authenticated :
		my_dict = dict(request.POST) #Request.POST est un QueryDict que l'on transforme en dict
		for cle, valeur in my_dict.items(): #On balaie le dictionnaire
			if valeur == ['Submit']: # Sans que je sache pourquoi le name de l'input dans ajax_modify_comment se retrouve en clé avec pour valeur ['Submit']
				name = cle           # Etant donné que le nom est composé comme "modifier_commentaire_{{ id_comment }}"
		type_button = name[:20] 
		id_comment = int(name[21:])
		commentaire = get_object_or_404(CommentSection, pk=id_comment)
		form = CommentSectionForm(request.POST, instance=commentaire)
		if form.is_valid():
			commentaire = form.save(commit=False)
			commentaire.modification = True
			commentaire.updated_at = datetime.datetime.now()
			commentaire.auteur_comment = request.user
			commentaire.nouvelle = post
			commentaire.save()
			messages.success(request, "Commentaire modifié ! On ne peut être parfait du premier coup ;) ")
			form = CommentSectionForm()
			return render(request, 'nouvelle/show.html', {'nouvelleecrite':post, 'form':form, 'nombre_mots':nombre_mots})
	else: 
		form = CommentSectionForm()
	return render(request, 'nouvelle/show.html', {'nouvelleecrite':post, 'form':form, 'nombre_mots':nombre_mots})




@csrf_exempt
def modify_comment(request): #Fonctionne avec requete ajax pour modifier un commentaire
	if request.is_ajax() and request.method == 'POST':
		id_comment = request.POST.get('id_comment', None) # On extrait l'id du commentaire à modifier
		commentaire = get_object_or_404(CommentSection, pk=id_comment)
		form = CommentSectionForm(instance=commentaire) # La form qui sera affichée
		modifier_commentaire_id = "modifier_commentaire_" + str(id_comment) # Pour le nom que l'on récupèrera avec l'id afin de savoir quel commentaire a été modifié cf show_blog 
		return render(request, 'nouvelle/ajax_modify_comment.html', {'form_comment' : form, 'modifier_commentaire_id': modifier_commentaire_id})

class NouvelleListView(ListView):
	model = NouvelleEcrite
	template_name = 'nouvelle/index.html'
	context_object_name = 'nouvelles_posts'
	
	def get_context_data(self, **kwargs): #Permet d'ajouter d'autres données ex : autre modèle
		context = super(NouvelleListView, self).get_context_data(**kwargs)
		context['tags'] = Tag.objects.all()
		type_tag = self.request.GET.get('tag', '')
		
		if type_tag != '' and type_tag != "Tous les tags":
			context['nouvelles_posts'] = Tag.objects.filter(tags=type_tag)[0].post_tags.all()
		for post in context['nouvelles_posts']:
			post.word_count =len(post.contenu.split()) 

		return context


class NouvelleCreateView(LoginRequiredMixin, CreateView):
	login_url = 'connexion:connexion'
	model = NouvelleEcrite
	form_class = NouvelleForm
	template_name = 'nouvelle/write_a_nouvelle.html'

	def form_valid(self, form): #Permet de fixer des valeurs du modèle
		form.instance.auteur_nouvelle = self.request.user
		form.instance.auteur_nouvelle.profile.nombre_post_ecrit += 1
		form.instance.auteur_nouvelle.profile.save()
		messages.success(self.request, "Youhou une nouvelle supplémentaire ! Bravo et merci de votre investissement et apport culturel certain ;)" )
		return super().form_valid(form)

class NouvelleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	login_url = 'connexion:connexion'
	model = NouvelleEcrite
	form_class = NouvelleForm
	template_name = 'nouvelle/modify_nouvelle.html'

	def form_valid(self, form): #Permet de fixer des valeurs du modèle
		form.instance.modification = True
		messages.success(self.request, "Nouvelle bien modifié, l'enrichissement et la qualité en sont sans nul doute plus grand :)" )
		return super().form_valid(form)

	def test_func(self): #Permet d'établir des conditions pour pouvoir faire l'action
		post = self.get_object()
		if self.request.user == post.auteur_nouvelle or self.request.user.is_superuser == True:
			return True
		return False

class NouvelleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = NouvelleEcrite
	login_url = 'connexion:connexion'

	def get_success_url(self): #Renvoie l'url en cas de succès
		user_profile = Profile.objects.get(user = self.request.user)
		user_profile.nombre_post_ecrit -= 1 
		user_profile.save()
		messages.error(self.request, "Nouvelle ... supprimée ... avec succès :( Pour la peine voilà du rouge ! Je vous avez pourtant dit de choisir la pillule bleue ... En espérant tout de même profiter d'un prochain article écrit par vos soins :)" )
		return reverse("nouvelle:index")

	def test_func(self): #Permet d'établir des conditions pour pouvoir faire l'action
		post = self.get_object()
		if self.request.user == post.auteur_nouvelle or self.request.user.is_superuser == True:
			return True
		return False


@csrf_exempt
def add_tag(request):
	new_tag = request.POST.get('new_tag', '')
	Tag(tags=new_tag).save()
	data = { 	
				'field' : NouvelleForm().visible_fields()[-1], 
				'form' : NouvelleForm(), 
	 		}
	return render(request, 'nouvelle/ajax_new_tag.html', data )


class NouvelleLikeToggle(LoginRequiredMixin, RedirectView):
	login_url = 'connexion:connexion'

	def get_redirect_url(self, *args, **kwargs):
		id_ = self.kwargs.get("id")
		post = get_object_or_404(NouvelleEcrite, pk=id_)
		url_ = post.get_absolute_url()
		user = self.request.user
		if user in post.likes.all():
			post.likes.remove(user)
		else:
			post.likes.add(user)
		return url_


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

class NouvelleLikeAPIToggle(APIView):
	"""
	View to list all users in the system.

	* Requires token authentication.
	* Only admin users are able to access this view.
	"""
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, id=None, slug=None, format=None):
		id_ = self.kwargs.get("id")
		post = get_object_or_404(NouvelleEcrite, id=id_)
		user = self.request.user
		updated = False
		liked = False
		if user.is_authenticated:
			if user in post.likes.all():
				liked = False
				post.likes.remove(user)
			else:
				liked = True
				post.likes.add(user)
			updated = True
		count = post.likes.count()
		data = {
		"updated": updated,
		"liked": liked,
		"count": count,
		}
		return Response(data)



class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = CommentSection
	login_url = 'connexion:connexion'

	def get_success_url(self): #Renvoie l'url en cas de succès
		post = self.get_object()
		messages.warning(self.request, "Commentaire supprimé :o Vous êtes donc allé jusqu'au bout, je ne sais si je dois saluer votre motivation :p J'espère quand même que ce n'était qu'un méchant commentaire :3")
		return  reverse("nouvelle:show", kwargs={'id':post.article.id, 'slug':post.article.slug})

	def test_func(self): #Permet d'établir des conditions pour pouvoir faire l'action
		post = self.get_object()
		if self.request.user.username == post.auteur_comment or self.request.user.is_superuser == True:
			return True
		return False

from django.core import serializers
from django.http import HttpResponse


def nuage_tag(request):
	if request.is_ajax() and request.method == 'GET':
		liste_tag = request.GET.getlist('liste_tag[]', None) # On extrait la liste d'id à prendre en compte
		# REMARQUE : utilisation de GETLIST pour obtenir une list et non un simple str
		tags = Tag.objects.all()
		nouvelle = NouvelleEcrite.objects.all()
		if liste_tag != None:
			liste_nom_tag = []
			for tag in liste_tag:
				nouvelle = nouvelle.filter(Q(tag=tag)) #Ajoute un filtre de choix en fonction des tags choisis
				liste_nom_tag.append(Tag.objects.get(id=tag).tags) #Ici on récupère le nom des tags sélectionnés
		for post in nouvelle:
			post.word_count =len(post.contenu.split()) #Nombre de mots dans chaque nouvelle 
		return render(request, 'nouvelle/ajax_tag_list.html', {'nouvelles_posts' : nouvelle, 'liste_tag': liste_nom_tag, 'tags' :tags})
import random
from django.http import JsonResponse
import string


def random_color(request):
	color_list = ['00', '10', '20', '30', '40', '50', '60', '70', '80', '90','A0', 'B0', 'C0', 'D0', 'E0', 'F0', 'FF']
	color = '#'
	less_bright = 0
	for i in range(3):
		if True in [i in string.ascii_lowercase for i in color]:
			less_bright = 7
		entier_random = random.randint(0,len(color_list)-1-less_bright)
		color = color + color_list[entier_random]
	data = { 'color_rand' : color}
	print('hey',data)
	return JsonResponse(data)