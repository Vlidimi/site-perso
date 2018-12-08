# Generated by Django 2.1.1 on 2018-11-28 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connexion', '0015_profile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/anonymous_image.png', height_field=100, max_length=200, upload_to='avatars/', width_field=100),
        ),
    ]
