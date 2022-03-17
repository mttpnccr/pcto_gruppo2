""" Gruppo 2 - Giuliano Antonenko - Panicciari Matteo
lambda_function
Lambda function for FindPlace intents
It takes attributes to search what you need and
response with a dictionary with most important information """
import json
import requests
import response_creator


def dict_request(location, info):
    """ Function to create the url address and use it with the API request """
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?" \
          "key=AIzaSyAUawfhWVYRe2WSgebqmzpbgUqmaDzzryI&" \
          f"type={info['place_type']}&" \
          f"location={location}&" \
          f"rankby={info['rankby']}"

    # add maxprice/minprice to the url address
    if info['maxprice'] != '':
        url = url + f"&maxprice={info['maxprice']}"
    elif info['minprice'] != '':
        url = url + f"&minprice={info['minprice']}"

    # add radius to the url address, 
    # if it isn't set and rankby is prominence, add default value (50000)
    if info['radius'] != '':
        url = url + f"&radius={info['radius']}"
    elif info['rankby'] == 'prominence':
        url = url + "&radius=50000"

    return requests.get(url).json()


def lambda_handler(event, context):
    """ Main, it takes input attributes and processes them with other function support """
    # input of the attributes from event queryStringParameters
    info = {'city': event['queryStringParameters']['city'],
            'place_type': event['queryStringParameters']['type'],
            'radius': event['queryStringParameters']['radius'],
            'maxprice': event['queryStringParameters']['maxprice'],
            'minprice': event['queryStringParameters']['minprice'],
            'rankby': event['queryStringParameters']['rankby']
    }

    # get location from city name
    result = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?"
                          f"address={info['city']}&"
                          f"key=AIzaSyAUawfhWVYRe2WSgebqmzpbgUqmaDzzryI").json()

    # get latitude and longitude from response dictionary
    lat = str(result['results'][0]['geometry']['location']['lat'])
    lon = str(result['results'][0]['geometry']['location']['lng'])

    # create attribute location joining lat ad lon
    location = lat + "%2C" + lon

    # calculation of the resulting dictionary of best attributes fitted place
    dict_response = dict_request(location, info)

    # call the function to create the response dictionary
    alexa_response = response_creator.create(dict_response['results'][0])

    if 'name' in alexa_response:
        return {
            'statusCode': 200,
            'body': json.dumps(alexa_response)
        }
    return {
        'statusCode': 400,  # Bad Request
        'body': json.dumps(alexa_response)
    }
