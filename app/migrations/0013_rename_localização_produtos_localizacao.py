# Generated by Django 4.2.7 on 2024-01-24 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_users_google_id_users_user_google'),
    ]

    operations = [
        migrations.RenameField(
            model_name='produtos',
            old_name='localização',
            new_name='localizacao',
        ),
    ]
