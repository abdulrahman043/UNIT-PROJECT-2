# Generated by Django 5.1.7 on 2025-03-19 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='images/profile_images/default.png', null=True, upload_to='images/profile_images/'),
        ),
    ]
