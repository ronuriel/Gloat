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
        [job_with_same_title for job_with_same_title in jobs_with_same_title]
        for job_with_same_title in jobs_with_same_title:
            skills_of_job_with_same_title = job_with_same_title.job_skills.all()
            [skill_of_job_with_same_title for skill_of_job_with_same_title in skills_of_job_with_same_title]
            skills_of_job_with_same_title_set = set()
            for skill_of_job_with_same_title in skills_of_job_with_same_title:
                skills_of_job_with_same_title_set.add(skill_of_job_with_same_title)
            if skills_set == skills_of_job_with_same_title_set:
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


def parameters_validation(params_keys):
    if len(params_keys) != 2:
        return {'valid_params': False,
                'response': {'invalid_job_object': 'job should contain 2 keys'}}

    if JOB_TITLE_KEY not in params_keys:
        return {'valid_params': False,
                'response': {'invalid_job_object': 'job should contain job_title key'}}

    if JOB_SKILLS_KEY not in params_keys:
        return {'valid_params': False,
                'response': {'invalid_job_object': 'job should contain job_skills key'}}

    return {'valid_params': True}



def get_job_2(request):
    title = request.GET.get(JOB_TITLE_KEY)
    skills_name = request.GET.get(JOB_SKILLS_KEY).split(',')
    skills = []
    for skill_name in skills_name:
        skill = Skill(skill_name=skill_name)
        skills.append(skill)

    job = Job(job_title=title)
    job.save()  #maybe should work with other object, reduce the save to db
    job.job_skills.set(skills)
    return job


class Candidate_Frequency:

    def __init__(self, candidate, frequency):
        self.candidate = candidate
        self.frequency = frequency


@api_view(['GET'])
def candidate_finder_2(request):
    #try/catch
    params_keys = request.GET.keys()
    valid_params = parameters_validation(params_keys)
    if valid_params['valid_params'] is False:
        return JsonResponse(valid_params['response'], status=status.HTTP_400_BAD_REQUEST)

    job_title = request.GET.get(JOB_TITLE_KEY)

    best_candidates_by_title = list(Candidate.objects.filter(candidate_title=job_title).all())

    #job_skills = job.job_skills.all()
    #[job_skill for job_skill in job_skills]

    job_skills = request.GET.get(JOB_SKILLS_KEY).split(',')
    #for skill in job_skills:
    #    skill = Skill(skill_name=skill)
    #    skills.append(skill)

    candidates_frequency = {}
    for job_skill in job_skills:
        skill_object = Skill.objects.filter(skill_name=job_skill).first()
        if skill_object is None:
            continue
        candidates_with_current_skill = skill_object.candidate_set.exclude(candidate_title=job_title).all()
        [candidate for candidate in candidates_with_current_skill]
        for candidate in candidates_with_current_skill:
            if candidate.id in candidates_frequency:
                candidates_frequency[candidate.id].frequency += 1
                #candidates_frequency[candidate.id] = [candidate, candidates_frequency[candidate.id][1] + 1] #make it class
            else:
                candidates_frequency[candidate.id] = Candidate_Frequency(candidate, 1)

    max_frequency = 0;
    best_candidates_by_skills = []
    for candidate_key in candidates_frequency.keys():
        current_candidate_frequency = candidates_frequency[candidate_key].frequency
        if current_candidate_frequency > max_frequency:
            best_candidates_by_skills = [candidates_frequency[candidate_key].candidate]
            max_frequency = current_candidate_frequency
        elif current_candidate_frequency == max_frequency:
            best_candidates_by_skills.append(candidates_frequency[candidate_key].candidate)

    #job.job_best_candidates.set(best_candidates_by_skills)
    best_candidates = best_candidates_by_title + best_candidates_by_skills
    return JsonResponse({'best_candidates': get_best_candidates_json(best_candidates)})


def parameters_validation_2(get_request):
    if len(get_request.keys()) != 1:
        return {'valid_params': False,
                'response': {'invalid parameters count': 'request should contain only a job id parameter'}}

    if 'id' not in get_request.keys():
        return {'valid_params': False,
                'response': {'invalid parameter key': 'the only parameter should be named id'}}

    if get_request.get('id').isnumeric() is False:
        return {'valid_params': False,
                'response': {'invalid parameter type': 'id should be a positive number'}}

    return {'valid_params': True}


def match_candidates(job):
    best_candidates_by_title = list(Candidate.objects.filter(candidate_title=job.job_title).all())

    candidates_frequency = {}
    job_skills = job.job_skills.all()
    [job_skill for job_skill in job_skills]
    for job_skill in job_skills:
        candidates_with_current_skill = job_skill.candidate_set.exclude(candidate_title=job.job_title).all()
        [candidate for candidate in candidates_with_current_skill]
        for candidate in candidates_with_current_skill:
            if candidate.id in candidates_frequency:
                candidates_frequency[candidate.id].frequency += 1
            else:
                candidates_frequency[candidate.id] = Candidate_Frequency(candidate, 1)

    max_frequency = 0
    best_candidates_by_skills = []
    for candidate_key in candidates_frequency.keys():
        current_candidate_frequency = candidates_frequency[candidate_key].frequency
        if current_candidate_frequency > max_frequency:
            best_candidates_by_skills = [candidates_frequency[candidate_key].candidate]
            max_frequency = current_candidate_frequency
        elif current_candidate_frequency == max_frequency:
            best_candidates_by_skills.append(candidates_frequency[candidate_key].candidate)

    # job.job_best_candidates.set(best_candidates_by_skills)
    return best_candidates_by_title + best_candidates_by_skills


@api_view(['GET'])
def candidate_finder_3(request):
    valid_params = parameters_validation_2(request.GET)
    if valid_params['valid_params'] is False:
        return JsonResponse(valid_params['response'], status=status.HTTP_400_BAD_REQUEST)

    job_id = request.GET.get('id')
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return JsonResponse({'invalid parameter value': 'Job does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({'best_candidates': get_best_candidates_json(match_candidates(job))})

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
        job_title = job.job_title
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
