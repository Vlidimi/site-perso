from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article, CommentSection

# @receiver(post_save, sender=Article)
# def create_comment(sender, instance, created, **kwargs):
#     if created:
#         CommentSection.objects.create(article=instance)

# @receiver(post_save, sender=Article)
# def save_comment(sender, instance, **kwargs):
#     instance.commentsection.save()