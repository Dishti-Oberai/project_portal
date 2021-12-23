# Generated by Django 3.2.5 on 2021-12-23 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_project_difficulty_alter_project_status'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='starred_projects',
            field=models.ManyToManyField(related_name='starred_projects', to='home.Project'),
        ),
    ]
