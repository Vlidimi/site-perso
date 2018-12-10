from django.shortcuts import render
from blog_livreSF.models import Article
from connexion.models import User, Profile

# Create your views here.

def home(request):
	pseudo_admin = Profile.objects.get(user=User.objects.get(username='Valentin'))
	last_posts = Article.objects.all()[:5]
	return render(request, 'pages/home.html', {'last_posts': last_posts, 'pseudo_admin' : pseudo_admin})