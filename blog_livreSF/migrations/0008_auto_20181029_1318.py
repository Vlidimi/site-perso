# Generated by Django 2.1.1 on 2018-10-29 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_livreSF', '0007_auto_20181029_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='source_contenu',
            field=models.URLField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name='article',
            name='source_resume',
            field=models.URLField(blank=True, max_length=2000),
        ),
    ]
