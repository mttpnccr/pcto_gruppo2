""" Gruppo 2 - Giuliano Antonenko - Matteo Panicciari
tasks for alexa developer console"""
import datetime  # to know the current time and turn date and hours in epoch time
import requests  # for request.get()


def main_route(slots):
    """ function to process attributes of CalculateRoute intent """
    # input of start and end address
    info = {
        'start': slots['start'].value,
        'end': slots['end'].value
    }

    # input and control of choice, if not set, it takes the value of dismin
    if slots['choice'].value is not None:
        info['choice'] = str(slots['choice'].slot_value.resolutions.
                             resolutions_per_authority[0].values[0].value.id)
    else:
        info['choice'] = 'durmin'

    # input and control of traffic, if not set, it takes the value of best_guess
    if slots['traffic'].value is not None:
        info['traffic'] = str(slots['traffic'].slot_value.resolutions.
                              resolutions_per_authority[0].values[0].value.id)
    else:
        info['traffic'] = 'best_guess'

    # input and control of mode, if not set, it takes the value of driving
    if slots['mode'].value is not None:
        info['mode'] = str(slots['mode'].slot_value.resolutions.
                           resolutions_per_authority[0].values[0].value.id)
    else:
        info['mode'] = 'driving'

    # url creation for lambda function
    url = f"https://dv4tw9y1xg.execute-api.eu-central-1.amazonaws.com/dev/maps?" \
          f"choice={info['choice']}&" \
          f"start={info['start']}&" \
          f"end={info['end']}&" \
          f"traffic={info['traffic']}&" \
          f"mode={info['mode']}&" \
          "departure_time="

    return requests.get(url).json()


def set_departure_time(hour):
    """ Function to turn datetime the departure hour in input to epoch time """
    # set the hour to the local zone
    now = str(datetime.datetime.today() + datetime.timedelta(hours=1))
    now_hm = now[11:16]  # Take only the part of hours and minutes

    # If that hour is passed, we will take that hour but of the following day
    if now_hm > hour:
        tomorrow = str(datetime.datetime.today() +
                       datetime.timedelta(hours=1) +  # local hour
                       datetime.timedelta(days=1))    # following day
        hour_res = datetime.datetime(int(tomorrow[:4]),     # year
                                     int(tomorrow[5:7]),    # month
                                     int(tomorrow[8:10]),   # day
                                     int(hour[:2]),         # hour and minute
                                     int(hour[-2:])).strftime('%s')
        mode = 'tomorrow'
    else:
        hour_res = datetime.datetime(int(now[:4]),     # year
                                     int(now[5:7]),    # month
                                     int(now[8:10]),   # day
                                     int(hour[:2]),    # hour and minute
                                     int(hour[-2:])).strftime('%s')
        mode = 'today'

    return {'response': hour_res, 'when': mode}


def main_compare(slots):
    """  Function to process attributes of CompareHours intent """
    # input of the attributes
    info = {
        'start': slots['departure'].value,
        'end': slots['arrival'].value,
        'first_time': slots['first_time'].value,
        'second_time': slots['second_time'].value,
        'third_time': slots['third_time'].value,
        'fourth_time': slots['fourth_time'].value
    }

    # set a standard url address must be completed with epoch departure time
    url = f"https://dv4tw9y1xg.execute-api.eu-central-1.amazonaws.com/dev/maps?choice=durmax&" \
          f"start={info['start']}&" \
          f"end={info['end']}&" \
          f"traffic=pessimistic&" \
          f"mode=driving&departure_time="

    # turn the hours into epoch format with set_departure_time() function
    first_hour = set_departure_time(info['first_time'])
    second_hour = set_departure_time(info['second_time'])
    third_hour = set_departure_time(info['third_time'])
    fourth_hour = set_departure_time(info['fourth_time'])
    
    
    # take the trip information leaving at the indicated time
    first_route = requests.get(url + first_hour['response']).json()
    second_route = requests.get(url + second_hour['response']).json()
    third_route = requests.get(url + third_hour['response']).json()
    fourth_route = requests.get(url + fourth_hour['response']).json()

    # add to the dictonaries the departure time in hour format
    first_route['hour'] = info['first_time']
    second_route['hour'] = info['second_time']
    third_route['hour'] = info['third_time']
    fourth_route['hour'] = info['fourth_time']

    # eventually add to the dictonary hour attribute the information 'di domani'
    if first_hour['when'] == 'tomorrow':
        first_route['hour'] += ' di domani'
    if second_hour['when'] == 'tomorrow':
        second_route['hour'] += ' di domani'
    if third_hour['when'] == 'tomorrow':
        third_route['hour'] += ' di domani'
    if fourth_hour['when'] == 'tomorrow':
        fourth_route['hour'] += ' di domani'

    return {'first_route': first_route, 'second_route': second_route, 'third_route': third_route,
            'fourth_route': fourth_route}


def main_place(slots):
    """  Function to process attributes of FindPlace intent """
    # input of the attributes
    info = {
        'city': slots['city'].value,
        'radius': slots['radius'].value,
        'place': slots['place'].slot_value.resolutions.resolutions_per_authority[0].values[0].value.id
    }

    # input and control of rankby, if not set, it takes the value of distance
    if slots['rankby'].value is not None:
        info['rankby'] = str(slots['rankby'].slot_value.resolutions.
                             resolutions_per_authority[0].values[0].value.id)
    else:
        info['rankby'] = 'distance'

    # input and control of radius
    if slots['radius'].value is not None:
        info['radius'] = slots['radius'].value
        info['rankby'] = 'prominence'
    else:
        info['radius'] = ''

    # input and control of maxprice, if not set, control minprice
    if slots['maxprice'].value is not None:
        info['maxprice'] = str(slots['maxprice'].slot_value.resolutions.
                               resolutions_per_authority[0].values[0].value.id)
        info['minprice'] = ''
    else:
        info['maxprice'] = ''
        if slots['minprice'].value is not None:
            info['minprice'] = str(slots['minprice'].slot_value.resolutions.
                                   resolutions_per_authority[0].values[0].value.id)
        else:
            info['minprice'] = ''

    # input and control of opennow, if not set, it takes the value of false
    if slots['opennow'].value is not None:
        info['opennow'] = str(slots['opennow'].slot_value.resolutions.
                              resolutions_per_authority[0].values[0].value.id)
    else:
        info['opennow'] = 'false'

    # creating url address with input attributes
    url = f"https://dv4tw9y1xg.execute-api.eu-central-1.amazonaws.com/dev/findplace?" \
          f"type={info['place']}&" \
          f"city={info['city']}&" \
          f"radius={info['radius']}&" \
          f"maxprice={info['maxprice']}&" \
          f"minprice={info['minprice']}&" \
          f"rankby={info['rankby']}"

    return requests.get(url).json()
