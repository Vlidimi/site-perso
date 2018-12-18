from django import forms
from .models import Article, CommentSection, Genre
import markdown
from connexion.models import User
class ArticleForm(forms.ModelForm):
	

    class Meta:
        model = Article
        exclude = ('auteur_blog','slug', 'date', 'likes', 'updated_at', 'modification', 'sous_genre',)
        # fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        # self.fields['name'].error_messages = {'required': 'custom required message'}

        # if you want to do it to all of them
        for field in self.fields.values():
            field.error_messages = {'required':'The field {fieldname} is required'.format(
                fieldname=field.label)}
        self.fields['contenu'].help_text = "Ecriture en markdown possible afin de structurer et d'accéder à des fonctionnalités d'HTML"
        self.fields['resume'].help_text = "Ecriture en markdown possible afin de structurer et d'accéder à des fonctionnalités d'HTML"
        self.fields['genre'].help_text = markdown.markdown("""Multiple sélection possible en appuyant sur la touche CTRL ! 
        	
         Vous ne trouvez pas le genre approprié à vos besoins ? Vous vous sentez frustré qu'il ne figure pas dans la liste ? Pas de panique ! Vous pouvez ajouter un genre en le renseigant plus bas ;)""")

    def clean(self):
        cleaned_data = super(ArticleForm, self).clean()
        titre = cleaned_data.get('titre')
        resume = cleaned_data.get('resume')
        contenu = cleaned_data.get('contenu')
		
        if titre in [i.titre for i in Article.objects.exclude(id=self.instance.id)]:
        	self.add_error("titre","Il semble que ce livre possède déjà un post le concernant. Allez le voir et n'hésitez pas à y mettre un commentaire ;)")
        if not resume and not contenu:
            # raise forms.ValidationError('You have to write something!')
            self.add_error("resume",'')
            self.add_error("contenu",'Il faut bien écrire un petit quelque chose ! Que ce soit un résumé ou du contenu')
        return cleaned_data
		
class CommentSectionForm(forms.ModelForm):
    class Meta:
        model = CommentSection
        fields = ('comment',)
        





class ContactForm(forms.Form):
    sujet = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    envoyeur = forms.EmailField(label="Votre adresse e-mail")
    renvoi = forms.BooleanField(help_text="Cochez si vous souhaitez obtenir une copie du mail envoyé.", required=False)

    def clean_message(self):
	    cleaned_data = super(ContactForm, self).clean()
	    sujet = cleaned_data.get('sujet')
	    message = cleaned_data.get('message')

	    if sujet and message:  # Est-ce que sujet et message sont valides ?
	        if "pizza" in sujet and "pizza" in message:
	            # raise forms.ValidationError(
	            #     "Vous parlez de pizzas dans le sujet ET le message ? Non mais ho !"
	            # )
	            self.add_error("message", 
                "Vous parlez déjà de pizzas dans le sujet, "
                "n'en parlez plus dans le message !"
            )



	    return cleaned_data  # N'oublions pas de renvoyer les données si tout est OK