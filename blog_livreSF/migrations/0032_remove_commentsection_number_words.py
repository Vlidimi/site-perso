# Generated by Django 2.1.1 on 2018-12-19 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_livreSF', '0031_commentsection_nombre_mots_afficher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentsection',
            name='number_words',
        ),
    ]
