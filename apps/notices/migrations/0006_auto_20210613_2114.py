# Generated by Django 2.2.24 on 2021-06-13 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0005_noticekind_enabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticekind',
            name='code',
            field=models.SlugField(help_text='Recuerde implementar la función con el mismo nombre en apps/notices/repository.py', max_length=32),
        ),
    ]
