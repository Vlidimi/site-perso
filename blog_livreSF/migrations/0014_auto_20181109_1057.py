# Generated by Django 2.1.1 on 2018-11-09 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_livreSF', '0013_auto_20181108_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='photo',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to='pictures/'),
        ),
    ]
