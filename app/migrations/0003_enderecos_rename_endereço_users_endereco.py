# Generated by Django 4.2.7 on 2024-01-14 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_users_data_create'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enderecos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.CharField(editable=False, max_length=250)),
                ('cidade', models.CharField(max_length=50)),
                ('bairro', models.CharField(max_length=50)),
                ('cep', models.IntegerField()),
                ('rua', models.CharField(max_length=100)),
                ('numero', models.IntegerField()),
            ],
        ),
        migrations.RenameField(
            model_name='users',
            old_name='endereço',
            new_name='endereco',
        ),
    ]
