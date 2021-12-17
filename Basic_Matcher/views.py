from django.shortcuts import render
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from Basic_Matcher.models import *
from rest_framework import status

JOB_TITLE_KEY = 'job_title' #capital letters
JOB_SKILLS_KEY = 'job_skills'


def skill_exists(skill_name):
    skill = Skill.objects.filter(skill_name=skill_name).first()
    if skill is not None:
        return {'exists': True,
                'skill': skill}

    return {'exists': False}


def get_job(request_body_json):
    title = request_body_json[JOB_TITLE_KEY]
    skills = []
    skills_set = set()
    added_new_skill_to_db = False
    for skill_name in request_body_json[JOB_SKILLS_KEY]:
        get_skill = skill_exists(skill_name)
        if get_skill['exists'] is True:
            skill = get_skill['skill']
            skills_set.add(skill)
        else:
            skill = Skill(skill_name=skill_name)
            skill.save()
            added_new_skill_to_db = True

        skills.append(skill)

    if added_new_skill_to_db is False:
        jobs_with_same_title = Job.objects.filter(job_title=title).all()
        if len(jobs_with_same_title) > 0:
            for job_with_same_title in jobs_with_same_title:
                skills_of_job_with_same_title = set(job_with_same_title.job_skills.all())
                if skills_set == skills_of_job_with_same_title:
                    return {'exists': True,
                            'job': job_with_same_title}

    job = Job(job_title=title)
    job.save()
    job.job_skills.set(skills)
    return {'exists': False,
            'job': job}


def get_best_candidates_json(best_candidates):
    best_candidates_json = []
    for candidate in best_candidates:
        best_candidates_json.append(get_candidate_json(candidate))

    return best_candidates_json


@api_view(['GET'])
def candidate_finder(request):
    request_body_json = json.loads(request.body)  # can be crashed?, think of change to parameters

    valid_body = body_validation(request_body_json)
    if valid_body['valid_body'] is False:
        return JsonResponse(valid_body['response'], status=status.HTTP_400_BAD_REQUEST)

    job_creation = get_job(request_body_json)
    job = job_creation['job']

    if job_creation['exists'] is True:
        job_best_candidates = job.job_best_candidates.all()
        return JsonResponse({'best_candidates': get_best_candidates_json(job_best_candidates)})
    else:
        job_title = request_body_json[JOB_TITLE_KEY]
        corresponding_candidates_title = Candidate.objects.filter(candidate_title=job_title).all()

        job_skills = request_body_json[JOB_SKILLS_KEY]

        best_candidates = []
        max_skills_intersection_length = 0
        for candidate in corresponding_candidates_title:
            candidate_skills = get_candidate_skills(candidate)
            current_skills_intersection_length = get_intersection_length(job_skills, candidate_skills)
            if current_skills_intersection_length > max_skills_intersection_length:
                best_candidates = [candidate]
                max_skills_intersection_length = current_skills_intersection_length

            elif current_skills_intersection_length == max_skills_intersection_length:
                best_candidates.append(candidate)

        job.job_best_candidates.set(best_candidates)
        return JsonResponse({'best_candidates': get_best_candidates_json(best_candidates)})


def body_validation(request_job_json):
    if len(request_job_json.keys()) != 2:
        return {'valid_body': False,
                'response': {'invalid_job_object': 'job should contain 2 keys'}}

    if JOB_TITLE_KEY not in request_job_json:
        return {'valid_body': False,
                'response': {'invalid_job_object': 'job should contain job_title key'}}

    if JOB_SKILLS_KEY not in request_job_json:
        return {'valid_body': False,
                'response': {'invalid_job_object': 'job should contain job_skills key'}}

    return {'valid_body': True}


def get_candidate_skills(candidate):
    candidate_skills = []
    for candidate_skill in candidate.candidate_skills.all():
        candidate_skills.append(candidate_skill.skill_name)

    return candidate_skills


def get_candidate_json(candidate_object):
    id = candidate_object.id
    title = candidate_object.candidate_title
    skills = []
    for skill in candidate_object.candidate_skills.all():
        skills.append(skill.skill_name)  # should return only the name or whole object

    return {'candidate_id': id,
            'candidate_title': title,
            'candidate_skills': skills}


def get_intersection_length(job_skills, candidate_skills):
    return len((set(job_skills)).intersection(set(candidate_skills))) #redundunt convert to set
