# Generated by Django 5.1.7 on 2025-03-27 01:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_profile_repost_of_delete_repost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='repost_of',
        ),
    ]
