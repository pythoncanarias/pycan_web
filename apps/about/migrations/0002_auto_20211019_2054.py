# Generated by Django 2.2.24 on 2021-10-19 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ally',
            options={'ordering': ['name']},
        ),
    ]
