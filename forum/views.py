from django.shortcuts import render
from connexion.models import User, Profile

# Create your views here.

def home(request):
	pseudo_admin = Profile.objects.get(user=User.objects.get(username='Valentin'))
	data = {'pseudo_admin' : pseudo_admin}
	return render(request, 'film/home.html', data)