# Generated by Django 5.1 on 2025-01-14 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('auteur', models.CharField(max_length=255)),
                ('genre', models.CharField(max_length=255)),
                ('annee_publication', models.IntegerField()),
                ('exemplaires_disponibles', models.PositiveIntegerField()),
                ('url_image', models.TextField()),
            ],
            options={
                'db_table': 'books',
            },
        ),
    ]
