# Generated by Django 2.1.1 on 2018-11-08 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_livreSF', '0010_auto_20181030_2113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='categorie',
        ),
        migrations.AlterField(
            model_name='article',
            name='photo',
            field=models.ImageField(max_length=200, upload_to='pictures/'),
        ),
    ]
