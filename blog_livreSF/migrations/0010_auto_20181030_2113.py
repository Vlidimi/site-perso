# Generated by Django 2.1.1 on 2018-10-30 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_livreSF', '0009_auto_20181030_2031'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-date'], 'verbose_name': 'article'},
        ),
        migrations.AddField(
            model_name='article',
            name='photo',
            field=models.ImageField(default='', upload_to='pictures/'),
        ),
    ]
