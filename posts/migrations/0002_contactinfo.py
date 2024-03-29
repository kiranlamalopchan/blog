# Generated by Django 3.2.8 on 2021-11-01 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_no', models.IntegerField(blank=True, null=True)),
                ('company', models.CharField(blank=True, max_length=100, null=True)),
                ('messages', models.TextField(max_length=5000, null=True)),
            ],
        ),
    ]
