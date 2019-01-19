from django.http import HttpResponse, JsonResponse

def response(code, data=[], message='', status=False, meta=None, errors=[], sys_errors=None):
    helpers = __import__("src.helper.helpers", globals(), locals(), ["decodeErrors"], 0)

    if meta==None and code==200:
        meta = {
            "page": 0,
            "limit": 0,
            "totalPages": 0,
            "totalRecords": 0
        }
    res_errors = []
    if errors:
        res_errors = helpers.decodeErrors(errors)
    else:
        if sys_errors:
            message=sys_errors

    res = {
        'code': code,
        'data': data,
        'meta': meta,
        'message': message,
        'errors': res_errors,
        'success' : status
    }
    return JsonResponse(res, status=code)

def setDefaultValue(field, data, default):
    return data[field] if field in data and data[field] != None else default