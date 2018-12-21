from django.urls import path, include

from . import views

app_name='nouvelle'
urlpatterns = [
	path('', views.NouvelleListView.as_view(), name='index'),
	path('<int:id>/<slug:slug>/update/', views.NouvelleUpdateView.as_view(), name='nouvelle-update'),
	path('<int:id>/<slug:slug>/delete/', views.NouvelleDeleteView.as_view(), name='nouvelle-delete'),
	path('write_a_nouvelle/', views.NouvelleCreateView.as_view(), name='write_a_nouvelle'),
	path('<int:id>/<slug:slug>/', views.show, name='show'),
	path('ajax/add_tag/', views.add_tag, name='add_tag'),
]