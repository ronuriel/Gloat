from Basic_Matcher.models import *


def match_candidates(job):
    #List all the the candidates that their title match to the given job's title
    best_candidates_by_title_queryset = Candidate.objects.filter(candidate_title=job.job_title).all()
    best_candidates_by_title = list(best_candidates_by_title_queryset)

    #List all other candidates that have the largest number of skill matching
    job_skills = job.job_skills.all()
    candidates_frequency = get_candidates_frequency(job, job_skills)
    best_candidates_by_skills = get_best_candidates_by_skill(candidates_frequency)

    #concatenating the two lists that represent the best matches to the given job
    return best_candidates_by_title + best_candidates_by_skills


def get_best_candidates_json(best_candidates):
    best_candidates_json = []
    for candidate in best_candidates:
        best_candidates_json.append(candidate.get_json())

    return best_candidates_json


def get_candidates_frequency(job, job_skills):
    candidates_frequency = {}
    for job_skill in job_skills:
        candidates_with_current_skill = job_skill.candidate_set.exclude(candidate_title=job.job_title).all()
        for candidate in candidates_with_current_skill:
            if candidate.id in candidates_frequency:
                candidates_frequency[candidate.id].frequency += 1
            else:
                candidates_frequency[candidate.id] = Candidate_Frequency(candidate, 1)

    return candidates_frequency


def get_best_candidates_by_skill(candidates_frequency):
    max_frequency = 0
    best_candidates = []
    for candidate_key in candidates_frequency.keys():
        current_candidate_frequency = candidates_frequency[candidate_key].frequency
        if current_candidate_frequency > max_frequency:
            best_candidates = [candidates_frequency[candidate_key].candidate]
            max_frequency = current_candidate_frequency
        elif current_candidate_frequency == max_frequency:
            best_candidates.append(candidates_frequency[candidate_key].candidate)

    return best_candidates
