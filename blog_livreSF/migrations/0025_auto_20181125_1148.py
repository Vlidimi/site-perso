# Generated by Django 2.1.1 on 2018-11-25 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_livreSF', '0024_article_sous_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='sous_genre',
            field=models.ManyToManyField(blank=True, related_name='post_sous_genre', to='blog_livreSF.Sous_Genre'),
        ),
    ]
