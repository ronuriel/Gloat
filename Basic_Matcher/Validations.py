def candidateFinder_parameters_validation(get_request):
    if len(get_request.keys()) != 1:
        return {'valid_params': False,
                'response': 'invalid parameters count: request should contain only a job id parameter'}

    if 'id' not in get_request.keys():
        return {'valid_params': False,
                'response': 'invalid parameter key: the only parameter should be named id'}

    param = get_request.get('id')
    if param.isnumeric() is False or param == '0':
        return {'valid_params': False,
                'response': 'invalid parameter type: id should be a positive integer'}

    return {'valid_params': True}