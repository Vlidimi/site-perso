from django.urls import path, include

from . import views

app_name='connexion'
urlpatterns = [
	path('se_connecter/', views.connexion, name='connexion'),
	path('enregistrement/', views.enregistrement, name='enregistrement'),
	path('deconnexion/', views.deconnexion, name='deconnexion'),

	path('profile/', views.user_profile, name='profile'),
	path('profile_change/', views.user_profile_change, name='profile-change'),
	path('profile/ajax/up_message_vu/', views.up_message_vu, name='up_message_vu'),
	path('ajax/message_non_lu/', views.message_non_lu, name='message_non_lu'),
	path('ajax/validate_username', views.validate_username, name='validate_username'),
	path('user_profile/<slug:slug>/', views.other_user, name='profile-other-user'),
    path('change_password/', views.change_password, name='change_password'),
    path('accounts/', include('django.contrib.auth.urls')),

	path('write_a_message/', views.sendmail, name='write_a_message'),
	path('write_a_message/<slug:slug>/', views.sendmail_destinataire, name='write_a_message_destinataire'),
	path('write_a_message/repondre/<str:pseudo>/', views.sendmail_repondre, name='write_a_message_repondre'),

	path('delete_mail/', views.suppr_mail, name='suppr_mail'),

]

    # path('accounts/', include('django.contrib.auth.urls') ),
