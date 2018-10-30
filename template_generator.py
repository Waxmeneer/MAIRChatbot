import csv
from LSTM import model_trainer, model_user
#Keep track of suggested restaurant if user wants another restaurant
#Make templates and keep track of order in which user states preferences
#aggregation?


#makes a list with lists of possible restaurants
#typical element in restaurant list is [name, pricerange, area, food, phone, addr, postcode]
def csv_reader():
    with open('restaurantinfo.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        restaurant_info = []
        for row in csv_reader:
            restaurant_info.append(list(row))
        restaurant_info.pop(0)
    return restaurant_info

def template_request(restaurant, sentence):
    possible_requests = {"phone": ["phone"],
                         "postcode": ["postcode", "post code"],
                         "addr": ["addr", "address"],
                         "price": ["price"],
                         "food": ["type"],
                         "area": ["area"]
    }
    restaurant = restaurant[0]
    info = ''
    for key, values in possible_requests.items():
        for value in values:
            if value in sentence:
                info = key

    if info == "phone":
        return "The phone number of {} is {} ".format(str(restaurant[0]), str(restaurant[4]))
    elif info == "addr":
        return "The address of {} is {} ".format(str(restaurant[0]), str(restaurant[5]))
    elif info == "postcode":
        return "The postcode of {} is {} ".format(str(restaurant[0]), str(restaurant[6]))
    elif info == "price":
        return "The price range of {} is {} ".format(str(restaurant[0]), str(restaurant[1]))
    elif info == "area":
        return "The {} is in the {} part of town ".format(str(restaurant[0]), str(restaurant[2]))
    elif info == "food":
        return "The food type of {} is {} ".format(str(restaurant[0]), str(restaurant[3]))
    else:
        return "Sorry, what information would you like to know about {}? Phone number, address, postcode, price range, area or type of food?".format(str(restaurant[0]))

def restaurant_finder(filled_slots, restaurant_info):
    possible_restaurants = []
    values_filled_slots = []

    #make list of slot values which are not None
    for key, value_list in filled_slots.items():
            value = value_list[0][0]
            if value == 'random':
                values_filled_slots.append(key)
            values_filled_slots.append(str(value))
    print(values_filled_slots, "these are the value filled slots")
    #make list of restaurant values and compare
    for restaurant in restaurant_info:
        info_elements = restaurant[1:4]
        if set(values_filled_slots).issubset(info_elements):
            possible_restaurants.append(restaurant)
    return possible_restaurants

def template_restart():
    return "What kind of restaurant would you like?"

def template_bye():
    return "Thank you for using team14 system. eet smakelijk!"

def template_hello():
    return "Welcome to the team14 restaurant system. You can tell your preference of area , price range or food type. How can we help?"

def template_inform_multiple_results(filled_slots, current_suggested_restaurant):
    response = 'There are {} restaurants found. '.format(len(current_suggested_restaurant))
    asked_slots = []
    try:
        filled_slots['pricerange']
    except KeyError:
        response += 'What is your price range? '
        asked_slots.append('pricerange')

    try:
        filled_slots['area']
    except KeyError:
        response += 'What is your area of preference? '
        asked_slots.append('area')

    try:
        filled_slots['food']
    except KeyError:
        response += 'What type of food would you like? '
        asked_slots.append('food')

    return [response, asked_slots]

def template_import_the_one(current_suggested_restaurant):
    current_suggested_restaurant = current_suggested_restaurant[0]
    name = str(current_suggested_restaurant[0])
    pricerange = str(current_suggested_restaurant[1])
    area = str(current_suggested_restaurant[2])
    food = str(current_suggested_restaurant[3])

    if area != '':
        return '{} is a {} {} restaurant in the {} area of town '.format(name, pricerange, food, area)
    else:
        return '{} is a {} {} restaurant'.format(name, pricerange, food)

def template_no_restaurant_found():
    return "We cannot find any restaurant. What other kind of restaurant you like?"

#gets if final restaurant or not (enkelvoud of meervoud zin teruggeven)
def template_generator(filled_slots, speech_act, current_suggested_restaurant, current_user_sentence):

    if speech_act == "hello":
        return template_hello()

    # if no preference / slots yet but the speech act is not inform, force them to give preference
    elif (not filled_slots) and (speech_act != 'inform'):
        return template_restart()

    elif speech_act == 'restart':
        return template_restart()

#joni:not restart, but search for another restaurant I guess while holding on to filled slots...
    elif speech_act == 'deny':
        return template_restart()

    elif (speech_act == "bye"):
        return template_bye()

    elif (speech_act == "thankyou"):
        return template_bye()

    elif speech_act == "request":

        if len(current_suggested_restaurant) == 0:
            return template_no_restaurant_found()

        # if 1 such restaurant exists: return restaurant info
        elif len(current_suggested_restaurant) == 1:
            return template_request(current_suggested_restaurant, current_user_sentence)

        # if more: return the number of restaurants and ask for missing slot info
        elif len(current_suggested_restaurant) > 1:
            return template_inform_multiple_results(filled_slots, current_suggested_restaurant)

    #negate is similar like inform, only usually started with "no"
    #reqmoe we can repeat the same answer for inform, only confirming
    #confirm  we can repeat the same answer for inform, only confirming
    #affirm this is also another way of confirming
    #ack use a lot words like "um" or "okay", another way of confirming or sometimes adding more info like "hmm how about korean?"
    #null super random, but when we return what we have in inform, it sounds still related
    #reqalts is very similar like inform

    elif speech_act == "inform" \
            or speech_act == "reqmore" \
            or speech_act == "negate" \
            or speech_act == "confirm" \
            or speech_act == "affirm"\
            or speech_act == "ack"\
            or speech_act == "null" \
            or speech_act == "reqalts":
        # if no restaurant exists with a complete slots: give back to user and ask other preferences
        if len(current_suggested_restaurant) == 0:
            return template_no_restaurant_found()

        # if 1 such restaurant exists: return restaurant
        elif len(current_suggested_restaurant) == 1:
            return template_import_the_one(current_suggested_restaurant)

        # if more: return the number of restaurants and ask for missing slot info
        elif len(current_suggested_restaurant) > 1:
            return template_inform_multiple_results(filled_slots, current_suggested_restaurant)

if __name__ == "__main__":
    #need to be filled in volgorde van de user als er geen slot is niks meegeven
    filled_slots = {
        "pricerange": "expensive",
        "area": "north",
        "food": "french"
    }
    restaurant_info = csv_reader()
    print(restaurant_finder(filled_slots, restaurant_info))
    #analyze speech act for every sentence
    #keep track of current restaurant
