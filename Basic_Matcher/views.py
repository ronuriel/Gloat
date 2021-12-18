from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework.decorators import api_view
from Basic_Matcher.models import *
from Basic_Matcher import Validations, Utils


@api_view(['GET'])
def candidate_finder(request):
    # validating the request's parameters
    valid_params = Validations.candidateFinder_parameters_validation(request.GET)
    if valid_params['valid_params'] is False:
        return HttpResponseBadRequest(valid_params['response'])

    #try to get the Job object from db by the given id
    job_id = request.GET.get('id')
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return HttpResponseBadRequest('invalid parameter value: Job does not exist')

    return JsonResponse({'best_candidates': Utils.get_best_candidates_json(Utils.match_candidates(job))})




























