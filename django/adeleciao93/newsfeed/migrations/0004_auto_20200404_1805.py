# Generated by Django 3.0.5 on 2020-04-04 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsfeed', '0003_auto_20200404_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_rating',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]
