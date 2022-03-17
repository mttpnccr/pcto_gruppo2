""" Gruppo 2 - Giuliano Antonenko - Panicciari Matteo
response_creator"""


def create(best_route, info):
    """ function to create response dictionary """

    # if there aren't legs
    if 'legs' in best_route:
        if 'duration_in_traffic' in best_route['legs'][0]:
            duration = best_route['legs'][0]['duration_in_traffic']['text']
        else:
            duration = best_route['legs'][0]['duration']['text']
        return {
            'start': info['start'],
            'end': info['end'],
            'choice': info['choice'],
            'mode': info['mode'],
            'traffic': info['traffic'],
            'distance': best_route['legs'][0]['distance']['text'],
            'duration': duration,
            'departure': info['departure_time']
        }

    if 'duration_in_traffic' in best_route:
        duration = best_route['duration_in_traffic']['text']
    else:
        duration = best_route['duration']['text']
    return {
        'start': info['start'],
        'end': info['end'],
        'choice': info['choice'],
        'mode': info['mode'],
        'traffic': info['traffic'],
        'distance': best_route['distance']['text'],
        'duration': duration,
        'departure': info['departure_time']
    }
