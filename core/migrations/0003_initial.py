# Generated by Django 5.1.7 on 2025-03-25 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_remove_category_parent_remove_profile_institution_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('subject', models.CharField(max_length=200, verbose_name='Sujet')),
                ('message', models.TextField(verbose_name='Message')),
                ('is_read', models.BooleanField(default=False, verbose_name='Lu')),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('is_active', models.BooleanField(default=True, verbose_name='Actif')),
            ],
            options={
                'verbose_name': 'Newsletter',
                'verbose_name_plural': 'Newsletters',
                'ordering': ['-created_at'],
            },
        ),
    ]
