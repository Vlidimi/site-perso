from django.urls import path
from .views import (
	PostListView,
	PostCreateView,
	PostUpdateView,
	PostDeleteView,
	PostDetailView,
	PostLikeToggle,
	CommentCreateView,
	CommentUpdateView,
	CommentDeleteView,
	PostLikeAPIToggle,
	add_genre,
)
from . import views

app_name='blog_livreSF'
# urlpatterns = [
# 	path('', views.index, name='index'),
# 	path('<int:id>/<slug:slug>', views.show, name='show'),
# 	path('<int:id>', views.show),
# 	path('write_a_blog/', views.write_a_blog, name='write_a_blog'),
# ]

urlpatterns = [
	path('', PostListView.as_view(), name='index'),
	path('<int:id>/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
	path('<int:id>/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
	path('noregister/<int:id>/<slug:slug>/', PostDetailView.as_view(), name='show-noregister'),
	path('<int:id>/<slug:slug>/', CommentCreateView.as_view(), name='show'),
	path('<int:id>/<slug:slug>/likes/', PostLikeToggle.as_view(), name='like-toggle'),
	path('api/<int:id>/<slug:slug>/likes/', PostLikeAPIToggle.as_view(), name='like-api-toggle'),
	path('<int:id>', CommentCreateView.as_view()),
	path('write_a_blog/', PostCreateView.as_view(), name='write_a_blog'),
	path('<int:id>/<slug:slug>/commentupdate/<int:pk>/', CommentUpdateView.as_view(), name='comment-update'),
	path('<int:id>/<slug:slug>/commentdelete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
	path('ajax/search/', views.search_title_auteur, name='ajax-search-titre'),
	path('ajax/add_genre/', views.add_genre, name='add_genre'),

]
