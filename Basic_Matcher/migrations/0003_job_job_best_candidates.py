# Generated by Django 4.0 on 2021-12-17 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Basic_Matcher', '0002_alter_skill_skill_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_best_candidates',
            field=models.ManyToManyField(to='Basic_Matcher.Candidate'),
        ),
    ]
