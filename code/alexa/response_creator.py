""" Gruppo 2 - Giuliano Antonenko - Matteo Panicciari
response_creator for alexa developer console"""


def res_calculate_route(response):
    """Set the alexa response of CalculateRoute from the dict obtained from the API request"""
    # Set choice
    if response['choice'] == 'dismin':
        choice = 'distanza minima'
    elif response['choice'] == 'dismax':
        choice = 'distanza massima'
    elif response['choice'] == 'durmin':
        choice = 'durata minima'
    elif response['choice'] == 'durmax':
        choice = 'durata massima'

    # Set mode
    if response['mode'] == 'driving':
        mode = 'in auto'
    elif response['mode'] == 'bicycling':
        mode = 'in bicicletta'
    elif response['mode'] == 'walking':
        mode = 'a piedi'
    elif response['mode'] == 'transit':
        mode = 'con i mezzi pubblici'

    # Set traffic, only if mode is driving or transit
    if response['mode'] == 'driving' or response['mode'] == 'transit':
        if response['traffic'] == 'best_guess':
            traffic = 'normale'
        elif response['traffic'] == 'optimistic':
            traffic = 'ottimistico'
        elif response['traffic'] == 'pessimistic':
            traffic = 'pessimistico'
        return f"Il percorso da {response['start']} a {response['end']} " \
               f"con {choice} prevede {response['distance']} e " \
               f"{response['duration']} di viaggio {mode} con traffico {traffic}."
    return f"Il percorso da {response['start']} a {response['end']} " \
           f"con {choice} prevede {response['distance']} e " \
           f"{response['duration']} di viaggio {mode}."


def res_compare_hours(dict_res):
    """Set the alexa response of CompareHours from the dict obtained from the API requests"""
    result = f"Il tragitto da " \
             f"{dict_res['first_route']['start']} a " \
             f"{dict_res['first_route']['end']} prevede " \
             f"{dict_res['first_route']['duration']} di viaggio partendo alle " \
             f"{dict_res['first_route']['hour']}, " \
             f"{dict_res['second_route']['duration']} partendo alle " \
             f"{dict_res['second_route']['hour']}, " \
             f"{dict_res['third_route']['duration']} partendo alle " \
             f"{dict_res['third_route']['hour']}, " \
             f"{dict_res['fourth_route']['duration']} partendo alle " \
             f"{dict_res['fourth_route']['hour']}"
    return result


def res_find_place(response):
    """Set the alexa response of FindPlace from the dict obtained from the API request"""
    
    str_address = ''
    str_open_now = ''
    str_price_level = ''
    str_rating = ''

    # set the address value splitting the old one in street name, civic number and city
    address = response['address'].split(', ')
    if len(address) == 1:
        str_address = f'a {address[0]}'
    if len(address) == 2:
        str_address = f'in {address[0]} a {address[1]}'
    if len(address) == 3:
        str_address = f'in {address[0]} numero {address[1]} a {address[2]}'
    if len(address) > 3:
        str_address = str(response['address'])

    # controls if 'open_now' atribute is in the dictionary
    # and his eventual value setting new variable
    if 'open_now' in response:
        if response['open_now'] is True:
            open_now = 'aperto'
        else:
            open_now = 'chiuso'

        str_open_now = f' In questo momento è {open_now}.'

    # controls if 'price_level' atribute is in the dictionary
    # and his eventual value setting new variable
    if 'price_level' in response:
        if response['price_level'] == 0:
            price_level = 'molto economico'
        elif response['price_level'] == 1:
            price_level = 'economico'
        elif response['price_level'] == 2:
            price_level = 'normale'
        elif response['price_level'] == 3:
            price_level = 'costoso'
        elif response['price_level'] == 4:
            price_level = 'molto costoso'

        str_price_level = f' Il suo costo è di tipo {price_level}.'

    # controls if 'rating' atribute is in the dictionary and his eventual value setting new variable
    if 'rating' in response:
        str_rating = f" Ha una valutazione media di {response['rating']}."

    return f"Il risultato trovato è " \
           f"{response['name']} " \
           f"{str_address}." \
           f"{str_open_now}{str_price_level}{str_rating}"
