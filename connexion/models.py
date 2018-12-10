from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    prenom = models.CharField(max_length=30, blank=True)
    nom = models.CharField(max_length=30, blank=True)
    pseudo = models.CharField(max_length=50, blank=True, default='JaiPasEncoreChoisiDePseudoCestPasBien')
    slug_pseudo = models.SlugField(max_length=40)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/",default='avatars/nobody.png', blank=True, max_length=200)
    signature = models.TextField(blank=True)
    nombre_post_ecrit = models.IntegerField(default=0)
    rang = models.CharField(max_length=50, default='Petite larve en devenir')
    bio = models.TextField(blank=True, default='')
    def __str__(self):
        return "Profil de {0}".format(self.user.username)

    def save(self, *args, **kwargs):
        self.slug_pseudo= slugify(self.pseudo) #Permet de générer un slug à partir d'une chaine de caractères
        super(Profile, self).save(*args, **kwargs) 

class MailBox(models.Model):
    expediteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expediteur")
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name="destinataire")
    message = models.TextField(blank=True, default='')
    objet_message = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now, 
                                verbose_name="Date de parution")
    message_lu = models.BooleanField(default=False)
    def __str__(self):
        return "De {0} à {1}".format(self.expediteur.username, self.destinataire.username)

    class Meta:
        ordering = ['-date'] #Ordonne par rapport à la date
