# Generated by Django 4.0 on 2021-12-17 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Basic_Matcher', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='skill_name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]