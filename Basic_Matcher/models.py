from django.db import models


class Skill(models.Model):
    skill_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.skill_name


class Candidate(models.Model):
    candidate_title = models.CharField(max_length=50)
    candidate_skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.candidate_title


class Job(models.Model):
    job_title = models.CharField(max_length=50)
    job_skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.job_title

