# Generated by Django 2.1.1 on 2018-11-26 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connexion', '0014_profile_slug_pseudo'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, default=''),
        ),
    ]
