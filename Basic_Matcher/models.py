from django.db import models


class Skill(models.Model):
    skill_name = models.CharField(max_length=50)


class Candidate(models.Model):
    candidate_title = models.CharField(max_length=50)
    candidate_skills = models.ManyToManyField(Skill)



class Job(models.Model):
    job_title = models.CharField(max_length=50)
    job_skills = models.ManyToManyField(Skill)

