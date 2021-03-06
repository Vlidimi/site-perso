from django.shortcuts import render, get_object_or_404, redirect, reverse
from blog_livreSF.models import Article, CommentSection, Genre
from .forms import ContactForm, ArticleForm, CommentSectionForm
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# import markdown
from connexion.models import Profile
import datetime
from django.views.decorators.csrf import csrf_exempt,csrf_protect 
from django.http import HttpResponse, JsonResponse



# Create your views here.

def index(request):
	posts = Article.objects.all()
	return render(request, 'blog_livreSF/index.html', {'posts': posts})

def show(request, id, slug = ''):
	post = get_object_or_404(Article, pk=id)
	return render(request, 'blog_livreSF/show.html', {'article': post, 'numero': id})

def show_blog(request, id, slug):
	post = get_object_or_404(Article, pk=id)
	nombre_mots = len(post.resume.split()) + len(post.contenu.split())
	if request.method == 'POST' and request.user.is_authenticated and 'laisser_commentaire' in request.POST:
	 	form = CommentSectionForm(request.POST)
	 	if form.is_valid():
	 		commentaire = form.save(commit=False)
	 		commentaire.auteur_comment = request.user
	 		commentaire.article = post
	 		commentaire.save()
	 		messages.success(request, "Commentaire envoyé ! Merci d'avoir pris le temps de partager votre avis :)")
	 		form = CommentSectionForm()
	 		return render(request, 'blog_livreSF/show.html', {'article':post, 'form':form, 'nombre_mots':nombre_mots})

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
			commentaire.article = post
			commentaire.save()
			messages.success(request, "Commentaire modifié ! On ne peut être parfait du premier coup ;) ")
			form = CommentSectionForm()
			return render(request, 'blog_livreSF/show.html', {'article':post, 'form':form, 'nombre_mots':nombre_mots})
	else: 
		form = CommentSectionForm()
	return render(request, 'blog_livreSF/show.html', {'article':post, 'form':form, 'nombre_mots':nombre_mots})




@csrf_exempt
def modify_comment(request): #Fonctionne avec requete ajax pour modifier un commentaire
	if request.is_ajax() and request.method == 'POST':
		id_comment = request.POST.get('id_comment', None) # On extrait l'id du commentaire à modifier
		commentaire = get_object_or_404(CommentSection, pk=id_comment)
		form = CommentSectionForm(instance=commentaire) # La form qui sera affichée
		modifier_commentaire_id = "modifier_commentaire_" + str(id_comment) # Pour le nom que l'on récupèrera avec l'id afin de savoir quel commentaire a été modifié cf show_blog 
		return render(request, 'blog_livreSF/ajax_modify_comment.html', {'form_comment' : form, 'modifier_commentaire_id': modifier_commentaire_id})


def write_a_blog(request):

	if request.method == 'POST':
		form = ArticleForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect("blog_livreSF:index")

	else:
		form = ArticleForm()
	return render(request, 'blog_livreSF/write_a_blog.html', {'form': form})




def search_title_auteur(request):
	
	search_text = request.GET.get('search_text', '')
	articles = Article.objects.filter(Q(titre__contains=search_text) | Q(auteur_livre__contains=search_text))
	return render(request, 'blog_livreSF/ajax_search_title_auteur.html', {'articles' : articles, "text": search_text})

@csrf_exempt
def add_genre(request):
	new_genre = request.POST.get('new_genre', '')
	if new_genre not in [i.genre_litteraire for i in Genre.objects.all()]:
		Genre(genre_litteraire=new_genre).save()
		data = { 	
					'field' : ArticleForm().visible_fields()[-1], 
					'form' : ArticleForm(), 
		 		}
		return render(request, 'blog_livreSF/ajax_new_genre.html', data )
	else:
		data = {'success': 'False'}
		return JsonResponse(data)





from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
	RedirectView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class PostListView(ListView):
	model = Article
	template_name = 'blog_livreSF/index.html'
	context_object_name = 'posts'
	# paginate_by = 2

	
	def get_context_data(self, **kwargs): #Permet d'ajouter d'autres données ex : autre modèle
		context = super(PostListView, self).get_context_data(**kwargs)
		context['genres'] = Genre.objects.all()
		type_genre = self.request.GET.get('genre', '')
		
		if type_genre != '' and type_genre != "Tous les genres":
			context['posts'] = Genre.objects.filter(genre_litteraire=type_genre)[0].post_genre.all()
		# context['page'] = self.request.GET.get('page', 1)
		# paginator = Paginator(context['posts'], 2)
		# context['paginator'] = paginator
		# try:
		# 	context['posts'] = paginator.page(context['page'])
		# except PageNotAnInteger:
		# 	context['posts'] = paginator.page(1)
		# except EmptyPage:
		# 	context['posts'] = paginator.page(paginator.num_pages)
		context['posts_len'] = []
		for post in context['posts']:
			post.word_count =len(post.resume.split()) + len(post.contenu.split())
		return context
	# ordering = ['-date']


class PostCreateView(LoginRequiredMixin, CreateView):
	login_url = 'connexion:connexion'
	model = Article
	form_class = ArticleForm
	template_name = 'blog_livreSF/write_a_blog.html'

	def form_valid(self, form): #Permet de fixer des valeurs du modèle
		form.instance.auteur_blog = self.request.user
		form.instance.auteur_blog.profile.nombre_post_ecrit += 1
		form.instance.auteur_blog.profile.save()
		messages.success(self.request, "Youhou un nouvel article ! Bravo et merci de votre investissement et apport culturel certain ;)" )
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	login_url = 'connexion:connexion'
	model = Article
	form_class = ArticleForm
	template_name = 'blog_livreSF/modify_blog.html'

	def form_valid(self, form): #Permet de fixer des valeurs du modèle
		form.instance.modification = True
		messages.success(self.request, "Article bien modifié, l'enrichissement et la qualité en sont sans nul doute plus grand :)" )
		return super().form_valid(form)

	def test_func(self): #Permet d'établir des conditions pour pouvoir faire l'action
		post = self.get_object()
		if self.request.user == post.auteur_blog or self.request.user.is_superuser == True:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Article
	login_url = 'connexion:connexion'

	def get_success_url(self): #Renvoie l'url en cas de succès
		user_profile = Profile.objects.get(user = self.request.user)
		user_profile.nombre_post_ecrit -= 1 
		user_profile.save()
		messages.error(self.request, "Article ... supprimé ... avec succès :( Pour la peine voilà du rouge ! Je vous avez pourtant dit de choisir la pillule bleue ... En espérant tout de même profiter d'un prochain article écrit par vos soins :)" )
		return reverse("blog_livreSF:index")

	def test_func(self): #Permet d'établir des conditions pour pouvoir faire l'action
		post = self.get_object()
		if self.request.user == post.auteur_blog or self.request.user.is_superuser == True:
			return True
		return False

# Le problème c'est que ça fait recharger toute la page. Ce qui n'est pas souhaitable
class PostLikeToggle(LoginRequiredMixin, RedirectView):
	login_url = 'connexion:connexion'

	def get_redirect_url(self, *args, **kwargs):
		id_ = self.kwargs.get("id")
		post = get_object_or_404(Article, pk=id_)
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

class PostLikeAPIToggle(APIView):
	"""
	View to list all users in the system.

	* Requires token authentication.
	* Only admin users are able to access this view.
	"""
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, id=None, slug=None, format=None):
		id_ = self.kwargs.get("id")
		post = get_object_or_404(Article, id=id_)
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
		return  reverse("blog_livreSF:show", kwargs={'id':post.article.id, 'slug':post.article.slug})

	def test_func(self): #Permet d'établir des conditions pour pouvoir faire l'action
		post = self.get_object()
		if self.request.user.username == post.auteur_comment or self.request.user.is_superuser == True:
			return True
		return False



# Désuet : 
#Poster un commentaire et afficher l'article
# class CommentCreateView(LoginRequiredMixin, CreateView):
# 	login_url = 'connexion:connexion'
# 	model = Article
# 	form_class = CommentSectionForm
# 	template_name = 'blog_livreSF/show.html'

# 	def form_valid(self, form): #Permet de fixer des valeurs du modèle
# 		form.instance.auteur_comment = User.objects.get(username = self.request.user)
# 		form.instance.article = self.get_object()
# 		messages.success(self.request, "Commentaire envoyé ! Merci d'avoir pris le temps de partager votre avis :)")
# 		return super().form_valid(form)

# 	def get_context_data(self, **kwargs): #Permet d'ajouter d'autres données ex : autre modèle
# 		context = super(CommentCreateView, self).get_context_data(**kwargs)
# 		context['article'] = self.get_object()
# 		context['modifier'] = False
# 		context['resume'] = markdown.markdown(context['article'].resume)
# 		context['contenu'] = markdown.markdown(context['article'].contenu)
# 		context['posts_len'] =len(context['article'].resume.split()) + len(context['article'].contenu.split())

# 		return context

# 	def test_func(self): #Permet d'établir des conditions pour pouvoir faire l'action
# 		post = self.get_object()
# 		if self.request.user.username == post.auteur_comment.username or self.request.user.is_superuser == True:
# 			return True
# 		else:
# 			return False


# 	def get_context_data(self, **kwargs): #Permet d'ajouter d'autres données ex : autre modèle
# 		context = super(CommentUpdateView, self).get_context_data(**kwargs)
# 		context['article'] = self.get_object().article
# 		context['comment_change'] = self.get_object()
# 		context['modifier'] = True
# 		return context
#Modifier un commentaire : fonction based view
# def show_blog_change_comment(request, id_article, id_comment, slug=''):
# 	post = get_object_or_404(Article, pk=id_article)
# 	comment = get_object_or_404(CommentSection, pk=id_comment)
# 	if request.method == 'POST' and request.user.is_authenticated:
# 	 	form = CommentSectionForm(request.POST, instance=comment)
# 	 	print(form, comment)
# 	 	if form.is_valid():
# 	 		print("hello")
# 	 		commentaire = form.save(commit=False)
# 	 		commentaire.auteur_comment = request.user
# 	 		commentaire.article = post
# 	 		commentaire.save()
# 	 		messages.success(request, "Commentaire modifié ! Merci d'avoir pris le temps de partager votre avis :)")
# 	 		form = CommentSectionForm()
# 	 		return render(request, 'blog_livreSF/show.html', {'article':post, 'form':form})
# 	else: 
# 		form = CommentSectionForm(instance=comment)
# 		print(form, comment)
# 	return render(request, 'blog_livreSF/modify_blog_bis.html', {'form':form, 'article': post})

# #Modifier un commentaire : class based view
# class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
# 	login_url = 'connexion:connexion'
# 	model = CommentSection
# 	form_class = CommentSectionForm
# 	template_name = 'blog_livreSF/show.html'

# 	def form_valid(self, form): #Permet de fixer des valeurs du modèle
# 		form.instance.modification = True
# 		messages.success(self.request, "Commentaire modifié ! On ne peut être parfait du premier coup ;) ")
# 		return super().form_valid(form)

# 	def test_func(self): #Permet d'établir des conditions pour pouvoir faire l'action
# 		post = self.get_object()
# 		if self.request.user.username == post.auteur_comment or self.request.user.is_superuser == True:
# 			return True
# 		else:
# 			return False


# 	def get_context_data(self, **kwargs): #Permet d'ajouter d'autres données ex : autre modèle
# 		context = super(CommentUpdateView, self).get_context_data(**kwargs)
# 		context['article'] = self.get_object().article
# 		context['comment_change'] = self.get_object()
# 		context['modifier'] = True
# 		return context
