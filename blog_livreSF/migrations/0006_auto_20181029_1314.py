# Generated by Django 2.1.1 on 2018-10-29 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_livreSF', '0005_auto_20181022_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='source_contenu',
            field=models.URLField(default=1, max_length=2000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='source_resume',
            field=models.URLField(default=True, max_length=2000),
            preserve_default=False,
        ),
    ]
