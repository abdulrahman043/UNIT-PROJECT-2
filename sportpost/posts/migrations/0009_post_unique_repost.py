# Generated by Django 5.1.7 on 2025-03-27 02:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_remove_post_reposted_by_post_repost_of'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='post',
            constraint=models.UniqueConstraint(condition=models.Q(('repost_of__isnull', False)), fields=('user', 'repost_of'), name='unique_repost'),
        ),
    ]
