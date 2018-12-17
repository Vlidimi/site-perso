from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Profile, User, MailBox
from .forms import (
	UserForm, ProfileForm, 
	UserUpdateForm, ProfileUpdateForm, 
	ConnexionForm,
	MailBoxForm, MailBoxFormBis, SupprMailForm)
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q

def suppr_mail(request):
	if request.method == "POST":
		form = SupprMailForm(request.POST)
		if form.is_valid():
			return redirect('home')
	else: 
		form = SupprMailForm()
	return render(request, 'connexion/delete_mail.html', {'form':form})

def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                return redirect('home')
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'connexion/se_connecter.html', locals())

def deconnexion(request):
    logout(request)
    return redirect('home')

def enregistrement(request):
	if request.method == 'POST':
		form = UserForm(request.POST)
		profile_form = ProfileForm(request.POST, request.FILES)
		if form.is_valid() and profile_form.is_valid():
			#Ici la problématique était de créer un profil qui correspondait
			#à un User renseigné sur la même page
			user = form.save() #Première étape, sauvegarder utilisateur 
			userprofile = profile_form.save(commit=False) #On sauvegarde le profile SANS L ENVOYER A LA DATABASE (car il n'a pas encore d'utilisateur associé !)
			userprofile.user = user # On renseigne l'utilisateur associé et maintenant on peut sauvegarder 
			userprofile.save()
			login(request, user)
			messages.success(request, 'Votre compte a bien été crée. Bienvenu :)')
			return redirect('home')
	else:
		form = UserForm()
		profile_form = ProfileForm()
	return render(request, 'connexion/enregistrement.html', {'form': form, 'profile_form': profile_form})

@login_required
def sendmail(request):
	if request.method == 'POST':
		form = MailBoxForm(request.POST)
		if form.is_valid():
			mail = MailBox()
			destinataire = Profile.objects.get(pseudo=form.cleaned_data['pseudo_destinataire'])
			mail.destinataire = destinataire.user
			mail.expediteur = request.user
			mail.message = form.cleaned_data['message']
			mail.objet_message = form.cleaned_data['objet_message']
			mail.save()
			return redirect('connexion:profile')
	else:
		form = MailBoxForm()
	return render(request, 'connexion/write_a_message.html', { 'form': form, })

@login_required
def sendmail_repondre(request, pseudo):

	if request.method == 'POST':
		form = MailBoxFormBis(request.POST)
		if form.is_valid():
			mail = MailBox()
			destinataire = Profile.objects.get(pseudo=pseudo)
			mail.destinataire = destinataire.user
			mail.expediteur = request.user
			mail.message = form.cleaned_data['message']
			mail.objet_message = form.cleaned_data['objet_message']
			mail.save()
			return redirect('connexion:profile')
	else:
		form = MailBoxFormBis()
	return render(request, 'connexion/write_a_message.html', { 'form': form, })

@login_required
def sendmail_destinataire(request, slug):
	if request.method == 'POST':
		form = MailBoxFormBis(request.POST)
		if form.is_valid():
			mail = MailBox()
			destinataire = Profile.objects.get(slug_pseudo=slug)
			mail.destinataire = destinataire.user
			mail.expediteur = request.user
			mail.message = form.cleaned_data['message']
			mail.objet_message = form.cleaned_data['objet_message']
			mail.save()
			return redirect('connexion:profile-other-user', slug=slug)
	else:
		form = MailBoxFormBis()
	return render(request, 'connexion/write_a_message.html', { 'form': form, })


@login_required
def user_profile_change(request):
	if request.method == 'POST':
		user_form = UserUpdateForm(request.POST, instance=request.user)
		profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Votre compte a bien été mis à jour')
			return redirect('connexion:profile')
	else:
		user_form = UserUpdateForm(instance=request.user)
		profile_form = ProfileUpdateForm(instance=request.user.profile)
	user_profile_ = User.objects.get(username=request.user)
	return render(request, 'connexion/profile_change.html', {'user_form': user_form, 'profile_form':profile_form, 'user_prof':user_profile_}) 

from django.http import JsonResponse

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

from django.views.decorators.csrf import csrf_exempt

@login_required
def up_message_vu(request):
	if request.method == "GET" and request.is_ajax():
		mailbox = MailBox.objects.filter(destinataire=request.user)
		id_message = request.GET.get('value_id', None)
		message = mailbox.get(id=id_message)
		message.message_lu = 'True'
		message.save()
		return render(request, 'connexion/ajax_change_message_lu.html', {'message_lu' : message.message_lu})
@login_required
def user_profile(request):
	profile = request.user.profile
	mailbox = MailBox.objects.filter(destinataire=request.user)
	if request.method == "GET" and request.is_ajax():
		dico_id_suppr = request.GET
		try:
			dico_id_suppr = dico_id_suppr.getlist('liste_value[]')
		except:
			error("Problème")	
		for id_suppr in dico_id_suppr:
			mailbox.filter(id=id_suppr).delete()
	return render(request, 'connexion/profile.html', {"profile":profile, "mailbox": mailbox} )

@login_required
def other_user(request, slug):
	profile = get_object_or_404(Profile, slug_pseudo=slug)	
	return render(request, 'connexion/profile.html', {"profile":profile})


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('connexion:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'connexion/change_password.html', {
        'form': form
    })


def message_non_lu(request):
	if request.is_ajax and request.method == 'GET':
		message_non_lu = MailBox.objects.filter(Q(destinataire=request.user) & Q(message_lu="False")).count()

		return render(request, 'connexion/ajax_message_non_lu.html', {'message_non_lu': message_non_lu} )

