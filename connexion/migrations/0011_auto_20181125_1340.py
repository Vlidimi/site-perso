# Generated by Django 2.1.1 on 2018-11-25 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connexion', '0010_auto_20181125_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/anonymous_image.png', max_length=200, upload_to='avatars/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='pseudo',
            field=models.CharField(blank=True, default='JaiPasEncoreChoisiDePseudoCestPasBien', max_length=50),
        ),
    ]
