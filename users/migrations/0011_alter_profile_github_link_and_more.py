# Generated by Django 4.0.1 on 2022-01-18 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_profile_github_link_profile_linked_in_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='github_link',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='linked_in_link',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='portfolio_link',
            field=models.TextField(blank=True),
        ),
    ]