from django.urls import path, include

from . import views

app_name='nouvelle'
urlpatterns = [
	path('', views.home, name='home')
]