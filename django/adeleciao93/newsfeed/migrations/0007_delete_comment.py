# Generated by Django 2.2.12 on 2020-04-05 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsfeed', '0006_vote'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
