""" Gruppo 2 - Giuliano Antonenko - Panicciari Matteo
response_creator"""


def create(place_found):
    """ function to create response dictionary """
    # add basic attributes to response
    response = {
        'name': place_found['name'],
        'address': place_found['vicinity']
    }
    
    # if these attributes are in place_found, add those to response
    if 'price_level' in place_found:
        response['price_level'] = place_found['price_level']
    if 'rating' in place_found:
        response['rating'] = place_found['rating']
    if 'opening_hours' in place_found:
        response['open_now'] = place_found['opening_hours']['open_now']

    return response
