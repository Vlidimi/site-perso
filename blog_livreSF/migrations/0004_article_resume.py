# Generated by Django 2.1.1 on 2018-10-22 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_livreSF', '0003_article_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='resume',
            field=models.TextField(null=True),
        ),
    ]
