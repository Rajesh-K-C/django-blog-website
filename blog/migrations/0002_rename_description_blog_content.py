# Generated by Django 5.0.6 on 2024-06-18 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='description',
            new_name='content',
        ),
    ]
