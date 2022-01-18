# Generated by Django 4.0.1 on 2022-01-18 05:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_profile_github_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cv',
            field=models.FileField(blank=True, upload_to='resumes', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
    ]
