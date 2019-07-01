from django.shortcuts import render
from django.http import QueryDict, HttpRequest, JsonResponse
from django.db.models import QuerySet, Count
from tester_matching.models import *
from typing import List, Dict

ALL_KW = "ALL"


def error_json(error_msg):
    '''
    When functioning as an API, I like to return verbose errors in JSON format.
    '''

    return JsonResponse({
        "error": error_msg,
    })


'''
This allows for choosing what to include in the JSON result, besides the necessary data.
'''
NON_ESSENTIAL_FIELDS = {
    'testerId__firstName': 'first_name',
    'testerId__lastName': 'last_name',
    'testerId__country': 'country',
    # 'testerId__lastLogin': 'last_login',
}


'''
This is a potential solution to a problem of too many string names in code.
At this scale it would potentially hurt the readability of the code, IMHO.
'''
# class _ESSENTIAL:
#     tester = 'testerId'
#     deviceDescription = 'deviceId__description'
#     submissions = 'submissions'
# ESSENTIAL_FIELDS = [
#     _ESSENTIAL.tester, _ESSENTIAL.deviceDescription, _ESSENTIAL.submissions
# ]


def parse_db_count_bugs(query_set) -> Dict:
    '''
    We expect ONLY these fields:
            'testerId',
            'deviceId__description',
            'submissions'
    Rest of the fields are considered non-essential and will be thrown into the object,
    if only they appear. E.g. 'testerId__firstName', 'testerId__lastName', etc.

    We return an unordered map like this:
        {5: {'first_name': 'Mingquan',
            'last_name': 'Zheng',
            'submissions': {'iPhone 4': 21},
            'total': 21},
        8: {'first_name': 'Sean',
            'last_name': 'Wellington',
            'country': "GB",
            'submissions': {'iPhone 4': 28, 'iPhone 5': 30}
            'total': 58}}
    '''

    result = {}
    for row in query_set:
        t_id = row['testerId']

        # defaultdict alternative
        if t_id not in result.keys():
            result[t_id] = {
                'submissions': {},
                'total': 0,
            }

            # adding non-essential keys
            for db_key, json_key in NON_ESSENTIAL_FIELDS.items():
                try:
                    result[t_id][json_key] = row[db_key]
                except:
                    continue

        # adding essential keys
        device = row['deviceId__description']
        bugs_count = row['submissions']
        result[t_id]['submissions'][device] = bugs_count
        result[t_id]['total'] += bugs_count

    return result


def search_db_count_bugs(countries: List[str], devices: List[str]) -> QuerySet:
    '''
    Given lists of countries and devices, returns a QuerySet of rows containing:
        'deviceId', 'testerId', 'deviceId__description', 'submissions'
        + some other defineable columns.
    Does not evaluate the QuerySet at any point,
    so whole workload should be performed by the DB engine.
    '''

    devices_ids_q = Device.objects.all()
    if ALL_KW not in devices:
        devices_ids_q = devices_ids_q.filter(description__in=devices)

    countries_ids_q = Tester.objects.values('country').distinct()
    if ALL_KW not in countries:
        countries_ids_q = countries_ids_q.filter(country__in=countries)

    # 1. select_related induces a JOIN
    # 2. filtering out according to countries and devices
    # 3. picking more fields to show
    # 4. counting bugs
    bug_count_q = Bug.objects.select_related('testerId', 'deviceId')\
        .filter(testerId__country__in=countries_ids_q)\
        .filter(deviceId__in=devices_ids_q)\
        .values('deviceId', 'testerId', 'deviceId__description', *NON_ESSENTIAL_FIELDS.keys())\
        .annotate(submissions=Count('bugId'))\
        .values('deviceId', 'testerId', 'deviceId__description', 'submissions', *NON_ESSENTIAL_FIELDS.keys())

    return bug_count_q


def post_search_json(request: HttpRequest):
    '''
    Reads POST data, retrieves the search results, returns it in JSON format.
    On error sends a JSON explaining what went wrong.
    '''

    try:
        countries = request.POST.getlist("countries")
        devices = request.POST.getlist("devices")
    except KeyError as e:
        return error_json(f"missing field {e.args[0]}")

    # further sanitization is not necessary, Django prevents SQL injections

    bugs_query_set = search_db_count_bugs(countries, devices)

    formatted_data = parse_db_count_bugs(bugs_query_set)

    return JsonResponse(formatted_data)
