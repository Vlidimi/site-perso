from django.urls import path, include

from . import views

app_name='film'
urlpatterns = [
	path('', views.home, name='home')
]