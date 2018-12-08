from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Genre(models.Model):
    genre_litteraire = models.CharField(max_length=30)

    def __str__(self):
        return self.genre_litteraire 

class Sous_Genre(models.Model):
    sous_genre_litteraire = models.CharField(max_length=30)
    genre_litteraire = models.ForeignKey(Genre, on_delete=models.CASCADE)
 
    def __str__(self):
        return "{0} dans la catégorie {1}".format(self.sous_genre_litteraire, self.genre_litteraire) 

class Article(models.Model):
    titre = models.CharField(max_length=100)
    auteur_livre = models.CharField(max_length=42)
    auteur_blog = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    resume = models.TextField(blank=True, default='')
    contenu = models.TextField(blank=True, default='') #null=True
    source_resume = models.CharField(blank=True, default='', max_length=2000)
    source_contenu = models.CharField(blank=True, default='', max_length=2000)
    photo = models.ImageField(upload_to="pictures/", blank=True,  max_length=200)
    date = models.DateTimeField(default=timezone.now, 
                                verbose_name="Date de parution")
    slug = models.SlugField(max_length=40)
    updated_at = models.DateTimeField(auto_now=True)
    modification = models.BooleanField(default=False)
    genre = models.ManyToManyField(Genre, blank=True, related_name='post_genre')
    sous_genre = models.ManyToManyField(Sous_Genre, blank=True, related_name='post_sous_genre')

    def save(self, *args, **kwargs):
        self.slug= slugify(self.titre) #Permet de générer un slug à partir d'une chaine de caractères
        super(Article, self).save(*args, **kwargs)    
    
    class Meta:
        verbose_name = "article"
        ordering = ['-date'] #Ordonne par rapport à la date
    
    def __str__(self):
        """ 
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que 
        nous traiterons plus tard dans l'administration
        """
        return self.titre

    def get_absolute_url(self):
        return reverse('blog_livreSF:show', kwargs={'id':self.id, 'slug':self.slug})

    def get_like_url(self):
        return reverse('blog_livreSF:like-toggle', kwargs={'id':self.id, 'slug':self.slug})

    def get_like_api_url(self):
        return reverse('blog_livreSF:like-api-toggle', kwargs={'id':self.id, 'slug':self.slug})


class CommentSection(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    auteur_comment = models.ForeignKey(User, on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.TextField()
    modification = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('blog_livreSF:show', kwargs={'id':self.article.id, 'slug':self.article.slug})

    def __str__(self):
        return self.auteur_comment.profile.pseudo #auteur_comment

    class Meta:
        verbose_name = "comment"
        ordering = ['-date']

