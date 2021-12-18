from django.db import models


class Skill(models.Model):
    skill_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.skill_name


class Candidate(models.Model):
    candidate_title = models.CharField(max_length=50)
    candidate_skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.candidate_title

    def get_json(self):
        skills = []
        candidate_skills = self.candidate_skills.all()
        [skill for skill in candidate_skills]
        for skill in candidate_skills:
            skills.append(skill.skill_name)

        return {'candidate_id': self.id,
                'candidate_title': self.candidate_title,
                'candidate_skills': skills}


class Job(models.Model):
    job_title = models.CharField(max_length=50)
    job_skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.job_title


class Candidate_Frequency:

    def __init__(self, candidate, frequency):
        self.candidate = candidate
        self.frequency = frequency

