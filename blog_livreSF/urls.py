from django.urls import path
from .views import (
	PostListView,
	PostCreateView,
	PostUpdateView,
	PostDeleteView,
	PostDetailView,
	PostLikeToggle,
	CommentDeleteView,
	PostLikeAPIToggle,
)
from . import views

app_name='blog_livreSF'

urlpatterns = [
	path('', PostListView.as_view(), name='index'),
	path('<int:id>/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
	path('<int:id>/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
	path('noregister/<int:id>/<slug:slug>/', PostDetailView.as_view(), name='show-noregister'),
	path('<int:id>/<slug:slug>/', views.show_blog, name='show'),
	path('<int:id>/<slug:slug>/likes/', PostLikeToggle.as_view(), name='like-toggle'),
	path('api/<int:id>/<slug:slug>/likes/', PostLikeAPIToggle.as_view(), name='like-api-toggle'),
	path('write_a_blog/', PostCreateView.as_view(), name='write_a_blog'),
	path('<int:id>/<slug:slug>/commentdelete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
	path('ajax/search/', views.search_title_auteur, name='ajax-search-titre'),
	path('ajax/add_genre/', views.add_genre, name='add_genre'),
	path('ajax/modify_comment/', views.modify_comment, name='ajax-modify-comment'),

]
