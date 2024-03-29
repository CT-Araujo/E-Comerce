# Generated by Django 4.2.7 on 2024-01-18 20:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_users_endereco'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('nome', models.CharField(max_length=50)),
                ('descricao', models.CharField(blank=True, max_length=50, null=True)),
                ('categoria', models.CharField(max_length=50)),
                ('loja', models.CharField(max_length=50)),
                ('preco', models.FloatField(max_length=5)),
                ('imposto', models.FloatField(max_length=5)),
                ('localização', models.CharField(max_length=50)),
            ],
        ),
    ]
