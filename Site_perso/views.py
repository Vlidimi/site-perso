from django.shortcuts import render
from blog_livreSF.models import Article
from nouvelle.models import NouvelleEcrite
from connexion.models import User, Profile

# Create your views here.

def home(request):
	pseudo_admin = Profile.objects.get(user=User.objects.get(username='Valentin'))
	last_posts = Article.objects.all()[:5]
	last_nouvelles = NouvelleEcrite.objects.all()[:5]
	return render(request, 'pages/home.html', {'last_posts': last_posts, 'last_nouvelles': last_nouvelles, 'pseudo_admin' : pseudo_admin})