from django import forms
from .models import NouvelleEcrite, CommentSection
from connexion.models import User
# import markdown

class NouvelleForm(forms.ModelForm):
	

    class Meta:
        model = NouvelleEcrite
        exclude = ('auteur_nouvelle','slug', 'date', 'likes', 'updated_at', 'modification',)
        # fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(NouvelleForm, self).__init__(*args, **kwargs)
        # self.fields['name'].error_messages = {'required': 'custom required message'}

        # if you want to do it to all of them
        for field in self.fields.values():
            field.error_messages = {'required':'The field {fieldname} is required'.format(
                fieldname=field.label)}

    def clean(self):
        cleaned_data = super(NouvelleForm, self).clean()
        titre = cleaned_data.get('titre')
        contenu = cleaned_data.get('contenu')
		
        if titre in [i.titre for i in NouvelleEcrite.objects.exclude(id=self.instance.id)]:
        	self.add_error("titre","Il semble que ce titre soit déjà pris :o Quel hasard ! Ou serait-ce voulu ? Quel qu'en soit la raison, veuillez faire preuve d'un peu d'originalité en en trouvant un autre svp :) (changer une seule lettre fonctionne ;p)")
        if not contenu:
            self.add_error("contenu","Il faut bien écrire un petit quelque chose ! Je ne me permettrai pas de douter de votre génie créatif mais quand même ... laissez le s'exprimer ;) ")
        return cleaned_data

class CommentSectionForm(forms.ModelForm):
    class Meta:
        model = CommentSection
        fields = ('comment',)