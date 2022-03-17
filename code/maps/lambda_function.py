""" Gruppo 2 - Giuliano Antonenko - Panicciari Matteo
lambda_function
Lambda function for CalculateRoute and CompareHours intents
It takes attributes for a trip and responses with a dictionary with all important information """
import json
import requests
import response_creator


def maxmin_finder(dict_response, choice):
    """ Function to find the route the user was looking for """

    # set of dir_dur
    if 'dur' in choice:
        dir_dur = 'duration'
    else:
        dir_dur = 'distance'

    # if there isn't any route we send an error message
    if len(dict_response['routes']) == 0:
        return 'error: nessun percorso trovato'

    # if there is only a route we haven't choice
    if len(dict_response['routes']) == 1:
        return dict_response['routes'][0]['legs'][0]

    # if there are more route we looking for the one which fits with choice
    result = dict_response['routes'][0]
    if 'max' in choice:
        for path in dict_response['routes'][1:]:
            if result['legs'][0][dir_dur]['value'] < path['legs'][0][dir_dur]['value']:
                result = path
    else:
        for path in dict_response['routes'][1:]:
            if result['legs'][0][dir_dur]['value'] > path['legs'][0][dir_dur]['value']:
                result = path
    return result


def dict_request(info):
    """ Function to create and get the result from the url with input parameters """
    url = "https://maps.googleapis.com/maps/api/directions/json?" \
          f"origin={info['start']}&" \
          f"destination={info['end']}&" \
          "units=metrical&" \
          "language=it&" \
          "alternatives=true&" \
          f"departure_time={info['departure_time']}&" \
          f"traffic_model={info['traffic']}&" \
          f"mode={info['mode']}&" \
          "key=AIzaSyAUawfhWVYRe2WSgebqmzpbgUqmaDzzryI"
    return requests.get(url).json()


def lambda_handler(event, context):
    """ Main, it takes input attributes and processes them with other function support """
    # input of the attributes from event queryStringParameters
    info = {'start': event['queryStringParameters']['start'],
            'end': event['queryStringParameters']['end'],
            'choice': event['queryStringParameters']['choice'],
            'mode': event['queryStringParameters']['mode'],
            'traffic': event['queryStringParameters']['traffic'],
            'departure_time': event['queryStringParameters']['departure_time']}

    # eventual setting of departure_time in current time if it isn't specified
    if info['departure_time'] == '':
        info['departure_time'] = requests.get('https://showcase.api.linx.twenty57.net/'
                                              'UnixTime/tounix?date=now').json()

    # calculation of the resulting dictionary of available paths
    dict_response = dict_request(info)

    # call the function to find the route we need
    alexa_response = maxmin_finder(dict_response, info['choice'])

    # check if there is an error on the request
    if 'bounds' in alexa_response:
        return {
            'statusCode': 200,
            # call the function to create the response dictionary
            'body': json.dumps(response_creator.create(alexa_response, info))
        }
    return {
        'statusCode': 400,  # Bad Request
        'body': json.dumps(alexa_response)
    }
