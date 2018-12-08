# Generated by Django 2.1.1 on 2018-11-14 22:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog_livreSF', '0015_auto_20181114_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='auteur_blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='article',
            name='auteur_livre',
            field=models.CharField(max_length=42),
        ),
    ]
