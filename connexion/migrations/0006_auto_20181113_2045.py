# Generated by Django 2.1.1 on 2018-11-13 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connexion', '0005_auto_20181113_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to='pictures/'),
        ),
    ]
