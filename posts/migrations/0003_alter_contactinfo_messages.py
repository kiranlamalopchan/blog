# Generated by Django 3.2.8 on 2021-11-01 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_contactinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfo',
            name='messages',
            field=models.TextField(max_length=500, null=True),
        ),
    ]
