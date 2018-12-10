from django import forms
from .models import Profile, User, MailBox
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime 
from django.forms import widgets
from django.template.defaultfilters import slugify
from django.db.models import Q



class UserForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget = widgets.SelectDateWidget(years=YEARS)

    class Meta:
        model = Profile
        fields = ('pseudo', 'avatar', 'prenom', 'nom', 'birth_date', 'signature')

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        if birth_date != None:
            if (datetime.now().year - birth_date.year)<6: 
                raise forms.ValidationError("Dis donc petit malin, tu bouches le bouchon un peu trop loin !")
            if (datetime.now().year - birth_date.year)>100:
                raise forms.ValidatizonError("Sans vouloir manquer de respect à votre ancienneté, j'ai comme l'impression que vous êtes entrain de m'entuber !")

        return birth_date
    def clean_pseudo(self):
        pseudo = self.cleaned_data['pseudo']
        if pseudo == 'JaiPasEncoreChoisiDePseudoCestPasBien':
            raise forms.ValidationError("Il faut choisir un peuso c'est important !")
        if Profile.objects.filter(slug_pseudo__iexact=slugify(pseudo)).exists():
            raise forms.ValidationError("Désolé mais ce pseudo est déjà pris")
        return pseudo


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email',)

YEARS= [x for x in range(datetime.now().year-122, datetime.now().year+1)]

class ProfileUpdateForm(forms.ModelForm):
    # birth_date = forms.DateField(label='Quelle est votre date de naissance ?', widget=forms.SelectDateWidget(years=YEARS))

    def __init__(self, *args, **kwargs):

        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.profile = self.instance
        self.fields['birth_date'].widget = widgets.SelectDateWidget(years=YEARS)

    class Meta:
        model = Profile
        fields = ('pseudo', 'avatar', 'prenom', 'nom', 'birth_date', 'signature', 'bio')

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        if birth_date != None:
            if (datetime.now().year - birth_date.year)<6:
                raise forms.ValidationError("Dis donc petit malin, tu bouches le bouchon un peu trop loin !")
            if (datetime.now().year - birth_date.year)>100:
                raise forms.ValidationError("Sans vouloir manquer de respect à votre ancienneté, j'ai comme l'impression que vous êtes entrain de m'entuber !")

        return birth_date

    def clean_pseudo(self):
        pseudo = self.cleaned_data['pseudo']
        if pseudo == 'JaiPasEncoreChoisiDePseudoCestPasBien':
            raise forms.ValidationError("Il faut choisir un peuso c'est important !")
        if Profile.objects.filter(Q(slug_pseudo__iexact=slugify(pseudo)) & ~Q(id__iexact=self.profile.id)).exists():
            raise forms.ValidationError("Désolé mais ce pseudo est déjà pris")
        if self.profile.user.username == pseudo:
            raise forms.ValidationError("Il vaut mieux que le nom d'utilisateur et le pseudo soient différents. Si vous tenez tant que ça à ce qu'ils soient identique, il n'est pas bien compliqué de faire sauter cette sécurité ;p")
        return pseudo

class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class MailBoxForm(forms.ModelForm):
    pseudo_destinataire = forms.CharField(label="Pseudo du destinataire", max_length=50)

    class Meta:
        model = MailBox
        fields = ['pseudo_destinataire', 'objet_message', 'message']

    def clean_pseudo_destinataire(self):
        pseudo_destinataire = self.cleaned_data['pseudo_destinataire']
        try:
            Profile.objects.get(pseudo=pseudo_destinataire)
            
        except:
            raise forms.ValidationError("Personne n'a ce pseudo. Si le problème persiste allez directement sur le profil de cette personne et cliquez sur 'envoyer un message'")

        return pseudo_destinataire

class MailBoxFormBis(forms.ModelForm):

    class Meta:
        model = MailBox
        fields = ['objet_message', 'message']

class SupprMailForm(forms.Form):
    num_list = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple())

    def __init__(self, *args, **kwargs):
        nombre_choix = kwargs.pop('instance', None)
        nombre_choix = nombre_choix.count()
        super(SupprMailForm, self).__init__(*args, **kwargs)
        num_choices = [[] for _ in range(nombre_choix)]
        for i in range(nombre_choix):
            num_choices[i] = (i, '')
        num_choices = tuple(num_choices)
        self.fields['num_list'].choices = num_choices

