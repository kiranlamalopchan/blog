# Generated by Django 3.2.9 on 2021-11-08 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_postview'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PostView',
        ),
    ]