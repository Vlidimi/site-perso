
from .forms import NouvelleForm
from .models import NouvelleEcrite, Tag
from connexion.models import Profile
from django.conf import settings
from django.contrib import messages
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
	print(post)
	return render(request, 'nouvelle/show.html', {'nouvelleecrite': post, 'numero': id})

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
		print(context)
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