from django.shortcuts import render
from blog_livreSF.models import Article

def home(request):
	last_posts = Article.objects.all()[:5]
	return render(request, 'pages/home.html', {'last_posts': last_posts})