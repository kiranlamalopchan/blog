# Generated by Django 3.2.9 on 2021-11-08 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_delete_postview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/img/authors'),
        ),
    ]
