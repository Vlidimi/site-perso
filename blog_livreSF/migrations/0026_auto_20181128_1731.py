# Generated by Django 2.1.1 on 2018-11-28 16:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog_livreSF', '0025_auto_20181125_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentsection',
            name='auteur_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='commentsection',
            name='comment',
            field=models.TextField(help_text='Laissez un commentaire :)'),
        ),
    ]
