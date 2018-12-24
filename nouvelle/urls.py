from django.urls import path, include

from . import views

app_name='nouvelle'
urlpatterns = [
	path('', views.NouvelleListView.as_view(), name='index'),
	path('<int:id>/<slug:slug>/update/', views.NouvelleUpdateView.as_view(), name='nouvelle-update'),
	path('<int:id>/<slug:slug>/delete/', views.NouvelleDeleteView.as_view(), name='nouvelle-delete'),
	path('write_a_nouvelle/', views.NouvelleCreateView.as_view(), name='write_a_nouvelle'),
	path('<int:id>/<slug:slug>/', views.show_blog, name='show'),
	path('ajax/add_tag/', views.add_tag, name='add_tag'),
	path('ajax/modify_comment/', views.modify_comment, name='ajax-modify-comment'),
	path('ajax/nuage_tag/', views.nuage_tag, name='ajax-tag'),
	path('ajax/random_color/', views.random_color),
	path('<int:id>/<slug:slug>/likes/', views.NouvelleLikeToggle.as_view(), name='like-toggle'),
	path('api/<int:id>/<slug:slug>/likes/', views.NouvelleLikeAPIToggle.as_view(), name='like-api-toggle'),
	path('<int:id>/<slug:slug>/commentdelete/<int:pk>/', views.CommentDeleteView.as_view(), name='comment-delete'),
]